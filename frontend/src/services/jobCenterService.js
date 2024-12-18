// src/services/jobCenterService.js
import apiRequest, { API_ENDPOINTS } from '../utils/apiUtils';

const BASE_URL = '/job-centers';

const handleError = (error, message) => {
  console.error(`Job Center Service Error - ${message}:`, error);
  if (error.response?.data?.detail) {
    throw new Error(error.response.data.detail);
  }
  throw error;
};

const jobCenterService = {
  getJobCenters: async () => {
    try {
      const response = await apiRequest.get(BASE_URL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleError(error, 'Error fetching job centers');
    }
  },

  getActiveJobCenters: async () => {
    try {
      const response = await apiRequest.get(`${BASE_URL}/active`, {
        headers: {
          'Accept': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleError(error, 'Error fetching active job centers');
    }
  },

  getJobCenterByWell: async (wellName) => {
    try {
      const response = await apiRequest.get(`${BASE_URL}/well/${wellName}`, {
        headers: {
          'Accept': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleError(error, 'Error fetching job center by well');
    }
  }
};

export default jobCenterService;

