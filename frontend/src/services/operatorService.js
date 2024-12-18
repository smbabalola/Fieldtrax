// src/services/operatorService.js
import apiRequest, { API_ENDPOINTS, handleApiError } from '../utils/apiUtils';

const operatorService = {
  getOperators: async (params = {}) => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.operators.getAll, {
        params
      });
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching operators');
    }
  },

  getOperatorByName: async (name) => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.operators.getByName(name));
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching operator by name');
    }
  }
};

export default operatorService;