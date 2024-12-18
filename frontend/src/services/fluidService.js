// src/services/fluidService.js
import apiRequest, { handleApiError } from '../utils/apiUtils';

const BASE_URL = '/fluids';

const fluidService = {
  getFluids: async (wellboreId) => {
    try {
      const response = await apiRequest.get(`${BASE_URL}/wellbore/${wellboreId}`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleApiError(error, 'Error fetching fluids');
    }
  },

  getFluidTypes: async (wellboreId, fluidType) => {
    try {
      const response = await apiRequest.get(`${BASE_URL}/wellbore/${wellboreId}/type/${fluidType}`, {
        headers: {
          'Accept': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleApiError(error, 'Error fetching fluid types');
    }
  },

  createFluid: async (fluidData) => {
    try {
      const response = await apiRequest.post(BASE_URL, fluidData, {
        headers: {
          'Accept': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleApiError(error, 'Error creating fluid');
    }
  },

  updateFluid: async (fluidId, fluidData) => {
    try {
      const response = await apiRequest.put(`${BASE_URL}/${fluidId}`, fluidData, {
        headers: {
          'Accept': 'application/json'
        }
      });
      return response;
    } catch (error) {
      handleApiError(error, 'Error updating fluid');
    }
  }
};

export default fluidService;