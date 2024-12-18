// src/services/rigService.js
import apiRequest, { API_ENDPOINTS, handleApiError } from '../utils/apiUtils';

const BASE_URL = API_ENDPOINTS.rigs.base;

const rigService = {
  getAllRigs: async () => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.rigs.getAll, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching rigs');
    }
  },

  getActiveRigs: async () => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.rigs.getActive);
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching active rigs');
    }
  }
};

export default rigService;