// src/utils/axios.js
import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    withCredentials: true  // Important for CORS
});

// Request interceptor
instance.interceptors.request.use(
    (config) => {
        // Add CORS headers to every request
        config.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000';
        config.headers['Access-Control-Allow-Credentials'] = 'true';
        
        // If URL starts with /api/v1, remove it since it's in baseURL
        if (config.url.startsWith('/api/v1')) {
            config.url = config.url.substring(7); // Remove /api/v1
        }
        
        console.log('Request:', {
            url: config.url,
            method: config.method,
            headers: config.headers,
            data: config.data
        });
        return config;
    },
    (error) => {
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
instance.interceptors.response.use(
    (response) => {
        console.log('Response:', response);
        return response;
    },
    (error) => {
        console.error('Response Error:', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data,
            headers: error.response?.headers
        });
        return Promise.reject(error);
    }
);

export default instance;