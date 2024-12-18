// src/services/wellService.js
import apiRequest, { API_ENDPOINTS, handleApiError } from '../utils/apiUtils';

const wellService = {
  getWells: async () => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.wells.getAll);
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching wells');
    }
  }
};

export default wellService;