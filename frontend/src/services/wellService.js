// File: /src/services/wellService.js
import apiRequest, { API_ENDPOINTS, handleApiError } from './api';

const wellService = {
  /**
   * Get all wells
   * @returns {Promise<Array>} Array of wells
   */
  getAllWells: async () => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.wells.getAll);
      return response;
    } catch (error) {
      handleApiError(error, 'Error fetching wells');
      return [];
    }
  },

  /**
   * Get wells by operator ID
   * @param {string|number} operatorId - The operator's ID
   * @returns {Promise<Array>} Array of wells belonging to the operator
   */
  getWellsByOperator: async (operatorId) => {
    try {
      if (!operatorId) {
        throw new Error('Operator ID is required');
      }
      const response = await apiRequest.get(API_ENDPOINTS.wells.getByOperator(operatorId));
      return Array.isArray(response) ? response : [];
    } catch (error) {
      handleApiError(error, 'Error fetching wells for operator');
      return [];
    }
  },

  /**
   * Get a single well by ID
   * @param {string|number} wellId - The well's ID
   * @returns {Promise<Object>} Well data
   */
  getWellById: async (wellId) => {
    try {
      if (!wellId) {
        throw new Error('Well ID is required');
      }
      const response = await apiRequest.get(`${API_ENDPOINTS.wells.base}/${wellId}`);
      return response;
    } catch (error) {
      handleApiError(error, 'Error fetching well details');
      throw error;
    }
  },

  /**
   * Create a new well
   * @param {Object} wellData - The well data to create
   * @returns {Promise<Object>} Created well data
   */
  createWell: async (wellData) => {
    try {
      if (!wellData.well_name) {
        throw new Error('Well name is required');
      }
      if (!wellData.operator_id) {
        throw new Error('Operator ID is required');
      }

      const response = await apiRequest.post(API_ENDPOINTS.wells.create, wellData);
      return response;
    } catch (error) {
      handleApiError(error, 'Error creating well');
      throw error;
    }
  },

  /**
   * Update an existing well
   * @param {string|number} wellId - The well's ID
   * @param {Object} wellData - The well data to update
   * @returns {Promise<Object>} Updated well data
   */
  updateWell: async (wellId, wellData) => {
    try {
      if (!wellId) {
        throw new Error('Well ID is required');
      }
      const response = await apiRequest.put(`${API_ENDPOINTS.wells.base}/${wellId}`, wellData);
      return response;
    } catch (error) {
      handleApiError(error, 'Error updating well');
      throw error;
    }
  },

  /**
   * Delete a well
   * @param {string|number} wellId - The well's ID
   * @returns {Promise<void>}
   */
  deleteWell: async (wellId) => {
    try {
      if (!wellId) {
        throw new Error('Well ID is required');
      }
      await apiRequest.delete(`${API_ENDPOINTS.wells.base}/${wellId}`);
    } catch (error) {
      handleApiError(error, 'Error deleting well');
      throw error;
    }
  },

  /**
   * Get wells by field name
   * @param {string} fieldName - The field name to search for
   * @returns {Promise<Array>} Array of wells in the specified field
   */
  getWellsByField: async (fieldName) => {
    try {
      if (!fieldName) {
        throw new Error('Field name is required');
      }
      const response = await apiRequest.get(`${API_ENDPOINTS.wells.base}/field/${fieldName}`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      handleApiError(error, 'Error fetching wells by field');
      return [];
    }
  },

  /**
   * Search wells by various criteria
   * @param {Object} searchParams - Search parameters
   * @returns {Promise<Array>} Array of matching wells
   */
  searchWells: async (searchParams) => {
    try {
      const queryString = new URLSearchParams(searchParams).toString();
      const response = await apiRequest.get(`${API_ENDPOINTS.wells.base}/search?${queryString}`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      handleApiError(error, 'Error searching wells');
      return [];
    }
  },

  /**
   * Validate well data before sending to the server
   * @param {Object} wellData - The well data to validate
   * @returns {Object} Validation result { isValid: boolean, errors: Object }
   */
  validateWellData: (wellData) => {
    const errors = {};
    
    if (!wellData.well_name?.trim()) {
      errors.well_name = 'Well name is required';
    }
    
    if (!wellData.operator_id) {
      errors.operator_id = 'Operator ID is required';
    }

    // Optional but recommended fields
    if (wellData.api_number && !wellData.api_number.match(/^[0-9-]+$/)) {
      errors.api_number = 'Invalid API number format';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }
};

export default wellService;