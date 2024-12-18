// src/utils/apiUtils.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  jobs: {
    base: '/jobs',
    getAll: '/jobs',
    getById: (id) => `/jobs/${id}`,
    create: '/jobs',
    update: (id) => `/jobs/${id}`,
    delete: (id) => `/jobs/${id}`,
    active: '/jobs/active',
    export: '/jobs/export'
  },
  operators: {
    base: '/operators',
    getAll: '/operators',
    getByName: (name) => `/operators/name/${name}`,
    getByCode: (code) => `/operators/code/${code}`
  },
  jobCenters: {
    base: '/job-centers',
    getAll: '/job-centers',
    getActive: '/job-centers/active',
    getByWell: (wellName) => `/job-centers/well/${wellName}`,
    getByShortName: (shortName) => `/job-centers/short/${shortName}`
  },
  wells: {
    base: '/wells',
    getAll: '/wells'
  },
  rigs: {
    base: '/rigs',
    getAll: '/rigs',
    getActive: '/rigs/active'
  },
  purchaseOrders: {
    base: '/purchase-orders',
    getAll: '/purchase-orders',
    getById: (id) => `/purchase-orders/${id}`
  }
};

const createApiRequest = () => {
  const instance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  });

  // Request interceptor
  instance.interceptors.request.use(
    (config) => {
      // Get token from localStorage
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      console.error('Request interceptor error:', error);
      return Promise.reject(error);
    }
  );

  // Response interceptor
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

export const handleApiError = (error, message) => {
  console.error(`API Error - ${message}:`, error);

  if (axios.isCancel(error)) {
    throw new Error('Request was cancelled');
  }

  if (error.code === 'ECONNABORTED') {
    throw new Error('Request timed out - please try again');
  }

  if (error.response?.data?.detail) {
    throw new Error(error.response.data.detail);
  }

  if (error.response) {
    const errorMessage = error.response.data?.message 
      || error.response.data?.detail 
      || `Server error: ${error.response.status}`;
    throw new Error(errorMessage);
  }

  if (error.request) {
    throw new Error('No response from server - please check your connection');
  }

  throw error;
};

export const apiRequest = createApiRequest();

export default apiRequest;