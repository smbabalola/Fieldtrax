# File: backend/app/core/rate_limit.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from typing import Dict, Tuple
from collections import defaultdict
import asyncio

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, Dict[str, Tuple[int, float]]] = defaultdict(dict)
        self.cleanup_task = None

    async def cleanup(self):
        """Remove old request records"""
        while True:
            current_time = time.time()
            for ip in list(self.requests.keys()):
                for path in list(self.requests[ip].keys()):
                    count, timestamp = self.requests[ip][path]
                    if current_time - timestamp > 3600:  # Clean after 1 hour
                        del self.requests[ip][path]
                if not self.requests[ip]:
                    del self.requests[ip]
            await asyncio.sleep(3600)  # Run cleanup every hour

    def is_allowed(self, ip: str, path: str, max_requests: int, window: int) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()
        if path in self.requests[ip]:
            count, timestamp = self.requests[ip][path]
            if current_time - timestamp > window:
                # Reset if window has passed
                self.requests[ip][path] = (1, current_time)
                return True
            if count >= max_requests:
                return False
            self.requests[ip][path] = (count + 1, timestamp)
        else:
            self.requests[ip][path] = (1, current_time)
        return True

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: RateLimiter):
        super().__init__(app)
        self.limiter = limiter

    async def dispatch(self, request: Request, call_next):
        # Define rate limits for different endpoints
        rate_limits = {
            "/api/v1/auth/login": (5, 300),  # 5 requests per 5 minutes
            "/api/v1/auth/forgot-password": (3, 3600),  # 3 requests per hour
            "/api/v1/auth/reset-password": (3, 3600),  # 3 requests per hour
            "/api/v1/auth/verify-email": (5, 3600),  # 5 requests per hour
        }

        path = request.url.path
        if path in rate_limits:
            max_requests, window = rate_limits[path]
            if not self.limiter.is_allowed(request.client.host, path, max_requests, window):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests, please try again later."}
                )

        response = await call_next(request)
        return response