// File: /frontend/src/services/cacheService.js
class CacheService {
    constructor() {
      this.cache = new Map();
      this.timeouts = new Map();
    }
  
    // Set cache with expiration
    set(key, data, expirationMinutes = 5) {
      this.cache.set(key, {
        data,
        timestamp: Date.now()
      });
  
      // Clear any existing timeout
      if (this.timeouts.has(key)) {
        clearTimeout(this.timeouts.get(key));
      }
  
      // Set new timeout
      const timeout = setTimeout(() => {
        this.delete(key);
      }, expirationMinutes * 60 * 1000);
  
      this.timeouts.set(key, timeout);
    }
  
    // Get cached data if not expired
    get(key, expirationMinutes = 5) {
      const cached = this.cache.get(key);
      if (!cached) return null;
  
      const now = Date.now();
      const age = (now - cached.timestamp) / 1000 / 60; // age in minutes
  
      if (age > expirationMinutes) {
        this.delete(key);
        return null;
      }
  
      return cached.data;
    }
  
    // Delete cache entry
    delete(key) {
      this.cache.delete(key);
      if (this.timeouts.has(key)) {
        clearTimeout(this.timeouts.get(key));
        this.timeouts.delete(key);
      }
    }
  
    // Clear all cache
    clear() {
      this.cache.clear();
      this.timeouts.forEach(timeout => clearTimeout(timeout));
      this.timeouts.clear();
    }
  
    // Check if cache exists and is valid
    isValid(key, expirationMinutes = 5) {
      const cached = this.cache.get(key);
      if (!cached) return false;
  
      const now = Date.now();
      const age = (now - cached.timestamp) / 1000 / 60;
      return age <= expirationMinutes;
    }
  }
  
  export const cacheService = new CacheService();
  
  // Cache-wrapped API request helper
  export const cachedApiRequest = async (key, apiCall, expirationMinutes = 5) => {
    const cached = cacheService.get(key, expirationMinutes);
    if (cached) {
      return cached;
    }
  
    const data = await apiCall();
    cacheService.set(key, data, expirationMinutes);
    return data;
  };