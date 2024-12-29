// File: /src/services/rigService.js
import api, { API_ENDPOINTS, handleApiError } from './api';
import { cacheService } from './cacheService';

// Cache keys
const CACHE_KEYS = {
  ALL_RIGS: 'all_rigs',
  ACTIVE_RIGS: 'active_rigs',
  RIG_DETAILS: (id) => `rig_${id}`,
  RIG_EQUIPMENT: (id) => `rig_equipment_${id}`
};

const rigService = {
  // Core Rig Operations
  getAllRigs: async (params = {}) => {
    try {
      const queryParams = {
        skip: params.skip || 0,
        limit: params.limit || 100,
        sort_field: params.sort_field || 'rig_name',
        sort_direction: params.sort_direction || 'asc',
        ...params
      };

      const response = await api.get(API_ENDPOINTS.rigs.getAll, { params: queryParams });
      return response.data;
    } catch (error) {
      console.error('Error fetching rigs:', error);
      throw error;
    }
  },

  getActiveRigs: async () => {
    try {
      const cached = cacheService.get(CACHE_KEYS.ACTIVE_RIGS);
      if (cached) return cached;

      const response = await api.get(API_ENDPOINTS.rigs.getActive);
      if (response) {
        cacheService.set(CACHE_KEYS.ACTIVE_RIGS, response, 5);
      }
      return response.data;
    } catch (error) {
      console.error('Error fetching active rigs:', error);
      throw error;
    }
  },

  getRigById: async (rigId) => {
    try {
      const cacheKey = CACHE_KEYS.RIG_DETAILS(rigId);
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await api.get(`${API_ENDPOINTS.rigs.base}/${rigId}`);
      if (response) {
        cacheService.set(cacheKey, response, 5);
      }
      return response.data;
    } catch (error) {
      console.error('Error fetching rig details:', error);
      throw error;
    }
  },

  createRig: async (rigData) => {
    try {
      const response = await api.post(API_ENDPOINTS.rigs.base, rigData);
      cacheService.clear();
      return response.data;
    } catch (error) {
      console.error('Error creating rig:', error);
      throw error;
    }
  },

  updateRig: async (rigId, rigData) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.rigs.base}/${rigId}`, rigData);
      cacheService.clear();
      return response.data;
    } catch (error) {
      console.error('Error updating rig:', error);
      throw error;
    }
  },

  deleteRig: async (rigId) => {
    try {
      await api.delete(`${API_ENDPOINTS.rigs.base}/${rigId}`);
      cacheService.clear();
    } catch (error) {
      console.error('Error deleting rig:', error);
      throw error;
    }
  },

  // Rig Equipment Operations
  getRigEquipment: async (rigId) => {
    try {
      const response = await api.get(API_ENDPOINTS.rigEquipment.getByRig(rigId));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching rig equipment');
    }
  },

  createRigEquipment: async (equipmentData) => {
    try {
      const response = await api.post(API_ENDPOINTS.rigEquipment.base, equipmentData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error creating rig equipment');
    }
  },

  updateRigEquipment: async (equipmentId, equipmentData) => {
    try {
      const response = await api.put(
        `${API_ENDPOINTS.rigEquipment.base}/${equipmentId}`, 
        equipmentData
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating rig equipment');
    }
  },

  // Mud Pump Operations
  getMudPumps: async (rigId) => {
    try {
      const response = await api.get(API_ENDPOINTS.mudPumps.getByRig(rigId));
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching mud pumps');
    }
  },

  getMudPumpBySerial: async (serialNumber) => {
    try {
      const response = await api.get(API_ENDPOINTS.mudPumps.getBySerial(serialNumber));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching mud pump');
    }
  },

  getMudPumpsByType: async (pumpType, rigId = null) => {
    try {
      const params = rigId ? { rig_id: rigId } : {};
      const response = await api.get(API_ENDPOINTS.mudPumps.getByType(pumpType), { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching mud pumps by type');
    }
  },

  // Rotary Equipment Operations
  getRotaryEquipment: async (rigId) => {
    try {
      const response = await api.get(API_ENDPOINTS.rotaryEquipment.getByRig(rigId));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching rotary equipment');
    }
  },

  getRotaryEquipmentByManufacturer: async (manufacturer) => {
    try {
      const response = await api.get(API_ENDPOINTS.rotaryEquipment.getByManufacturer(manufacturer));
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rotary equipment by manufacturer');
    }
  },

  getRotaryEquipmentByPower: async (minPower) => {
    try {
      const response = await api.get(API_ENDPOINTS.rotaryEquipment.getByPower(minPower));
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rotary equipment by power');
    }
  },

  // Well Control Equipment Operations
  getWellControlEquipment: async (rigId) => {
    try {
      const response = await api.get(API_ENDPOINTS.wellControlEquipment.getByRig(rigId));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching well control equipment');
    }
  },

  getWellControlEquipmentByPressure: async (minPressure) => {
    try {
      const response = await api.get(API_ENDPOINTS.wellControlEquipment.getByPressure(minPressure));
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching well control equipment by pressure');
    }
  },

  getWellControlEquipmentSpecifications: async (equipmentId) => {
    try {
      const response = await api.get(API_ENDPOINTS.wellControlEquipment.getSpecifications(equipmentId));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching well control equipment specifications');
    }
  },

  // Rig Stability Operations
  getRigStability: async (rigId) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.rigs.base}/${rigId}/stability`);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching rig stability');
    }
  },

  // Rig Type Operations
  getRigTypes: async (params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.rigTypes.getAll, { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rig types');
    }
  },

  createRigType: async (typeData) => {
    try {
      const response = await api.post(API_ENDPOINTS.rigTypes.base, typeData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error creating rig type');
    }
  },

  updateRigType: async (typeId, typeData) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.rigTypes.base}/${typeId}`, typeData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating rig type');
    }
  },

  // Batch Operations
  batchUpdateRigs: async (updates) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.rigs.base}/batch`, updates);
      cacheService.clear();
      return response;
    } catch (error) {
      return handleApiError(error, 'Error performing batch update');
    }
  },

  // Validation
  validateRigData: (data) => {
    const errors = {};

    if (!data.rig_name?.trim()) {
      errors.rig_name = 'Rig name is required';
    }

    if (!data.rig_type_id) {
      errors.rig_type_id = 'Rig type is required';
    }

    // Validate capacities if provided
    if (data.max_hook_load && isNaN(Number(data.max_hook_load))) {
      errors.max_hook_load = 'Maximum hook load must be a number';
    }

    if (data.max_drilling_depth && isNaN(Number(data.max_drilling_depth))) {
      errors.max_drilling_depth = 'Maximum drilling depth must be a number';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  },

  /**
   * Get rigs by contractor ID
   * @param {string} contractorId Contractor ID
   * @returns {Promise<Array>} List of rigs
   */
  getRigsByContractor: async (contractorId) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.rigs.getByContractor}/${contractorId}`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rigs by contractor');
    }
  },

  /**
   * Get rigs by location
   * @param {string} location Location name
   * @returns {Promise<Array>} List of rigs
   */
  getRigsByLocation: async (location) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.rigs.getByLocation}/${location}`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rigs by location');
    }
  },

  // Rig Retrieval by Type
  getByType: async (typeId) => {
    try {
      const response = await api.get(API_ENDPOINTS.rigs.getByType(typeId));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching rigs by type');
    }
  },

  /**
   * Get rigs by status
   * @param {string} status Rig status
   * @returns {Promise<Array>} List of rigs
   */
  getRigsByStatus: async (status) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.rigs.getByStatus}/${status}`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching rigs by status');
    }
  },

  // Rig Deletion
  delete: async (id) => {
    try {
      const response = await api.delete(API_ENDPOINTS.rigs.delete(id));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error deleting rig');
    }
  }
};

export default rigService;