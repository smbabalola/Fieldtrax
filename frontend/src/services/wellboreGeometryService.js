// src/services/wellboreGeometryService.js
import axios from '../services/api';
import api from './api';

const WELLBORE_API_URL = '/wellbore-geometry';

const transformTubularData = (data) => ({
  outer_diameter: data.outer_diameter ? Number(data.outer_diameter) : null,
  inner_diameter: data.inner_diameter ? Number(data.inner_diameter) : null,
  weight: data.weight ? Number(data.weight) : null,
  grade: data.grade || null,
  thread: data.thread || null,
  open_hole_size: data.open_hole_size ? Number(data.open_hole_size) : null,
  yield_strength: data.yield_strength ? Number(data.yield_strength) : null,
  capacity: data.capacity ? Number(data.capacity) : null,
  volume: data.volume ? Number(data.volume) : null,
  burst: data.burst ? Number(data.burst) : null,
  collapse: data.collapse ? Number(data.collapse) : null,
  drift: data.drift ? Number(data.drift) : null,
  start_depth: data.start_depth ? Number(data.start_depth) : null,
  end_depth: data.end_depth ? Number(data.end_depth) : null,
  remarks: data.remarks || null
});

const transformCasingData = (data) => ({
  ...transformTubularData(data),
  cement_top: data.cement_top ? Number(data.cement_top) : null,
  cement_yield: data.cement_yield ? Number(data.cement_yield) : null
});

const transformLinerData = (data) => ({
  ...transformTubularData(data),
  liner_top: data.liner_top ? Number(data.liner_top) : null,
  liner_bottom: data.liner_bottom ? Number(data.liner_bottom) : null,
  bht_at_liner_top: data.bht_at_liner_top ? Number(data.bht_at_liner_top) : null,
  liner_top_depth: data.liner_top_depth ? Number(data.liner_top_depth) : null,
  liner_top_deviation: data.liner_top_deviation ? Number(data.liner_top_deviation) : null,
  liner_shoe_deviation: data.liner_shoe_deviation ? Number(data.liner_shoe_deviation) : null,
  liner_Overlap_length: data.liner_Overlap_length ? Number(data.liner_Overlap_length) : null
});

const handleError = (error, customMessage) => {
  console.error('API Error:', error);
  
  if (axios.isCancel(error)) {
    throw new Error('Request was cancelled');
  }

  if (error.response?.data?.detail) {
    throw new Error(error.response.data.detail);
  }

  throw new Error(customMessage || 'An unexpected error occurred');
};

const wellboreGeometryService = {
  // Casing Operations
  getCasings: async (wellboreId) => {
    try {
      const response = await axios.get(`${WELLBORE_API_URL}/${wellboreId}/casings`);
      return response.data.map(transformCasingData);
    } catch (error) {
      handleError(error, 'Failed to fetch casings');
    }
  },

  addCasing: async (wellboreId, casingData) => {
    try {
      const transformedData = transformCasingData(casingData);
      const response = await axios.post(
        `${WELLBORE_API_URL}/${wellboreId}/casings`, 
        transformedData
      );
      return transformCasingData(response.data);
    } catch (error) {
      handleError(error, 'Failed to add casing');
    }
  },

  updateCasing: async (casingId, casingData) => {
    try {
      const transformedData = transformCasingData(casingData);
      const response = await axios.put(
        `${WELLBORE_API_URL}/casings/${casingId}`, 
        transformedData
      );
      return transformCasingData(response.data);
    } catch (error) {
      handleError(error, 'Failed to update casing');
    }
  },

  deleteCasing: async (casingId) => {
    try {
      await axios.delete(`${WELLBORE_API_URL}/casings/${casingId}`);
      return true;
    } catch (error) {
      handleError(error, 'Failed to delete casing');
    }
  },

  // Liner Operations
  getLiners: async (wellboreId) => {
    try {
      const response = await axios.get(`${WELLBORE_API_URL}/${wellboreId}/liners`);
      return response.data.map(transformLinerData);
    } catch (error) {
      handleError(error, 'Failed to fetch liners');
    }
  },

  addLiner: async (wellboreId, linerData) => {
    try {
      const transformedData = transformLinerData(linerData);
      const response = await axios.post(
        `${WELLBORE_API_URL}/${wellboreId}/liners`, 
        transformedData
      );
      return transformLinerData(response.data);
    } catch (error) {
      handleError(error, 'Failed to add liner');
    }
  },

  updateLiner: async (linerId, linerData) => {
    try {
      const transformedData = transformLinerData(linerData);
      const response = await axios.put(
        `${WELLBORE_API_URL}/liners/${linerId}`, 
        transformedData
      );
      return transformLinerData(response.data);
    } catch (error) {
      handleError(error, 'Failed to update liner');
    }
  },

  deleteLiner: async (linerId) => {
    try {
      await axios.delete(`${WELLBORE_API_URL}/liners/${linerId}`);
      return true;
    } catch (error) {
      handleError(error, 'Failed to delete liner');
    }
  },

  // Combined Wellbore Geometry Operations
  getWellboreGeometry: async (wellboreId) => {
    try {
      const [casings, liners] = await Promise.all([
        wellboreGeometryService.getCasings(wellboreId),
        wellboreGeometryService.getLiners(wellboreId)
      ]);
      
      return {
        casings,
        liners
      };
    } catch (error) {
      handleError(error, 'Failed to fetch wellbore geometry');
    }
  },

  /**
   * Get wellbore geometry by type
   * @param {string} wellboreId Wellbore ID
   * @param {string} type Geometry type (e.g., 'casing', 'liner')
   * @returns {Promise<Array>} List of wellbore geometry items
   */
  getWellboreGeometryByType: async (wellboreId, type) => {
    try {
      const response = await axios.get(`${WELLBORE_API_URL}/${wellboreId}/${type}`);
      return Array.isArray(response.data) ? response.data : [];
    } catch (error) {
      handleError(error, `Failed to fetch wellbore geometry by type: ${type}`);
    }
  },

  /**
   * Get wellbore geometry summary
   * @param {string} wellboreId Wellbore ID
   * @returns {Promise<Object>} Wellbore geometry summary
   */
  getWellboreGeometrySummary: async (wellboreId) => {
    try {
      const response = await axios.get(`${WELLBORE_API_URL}/${wellboreId}/summary`);
      return response.data;
    } catch (error) {
      handleError(error, 'Failed to fetch wellbore geometry summary');
    }
  },

  // Wellbore Operations
  createWellbore: async (wellboreData) => {
    try {
      const response = await api.post('/wellbores', wellboreData);
      return response.data;
    } catch (error) {
      console.error('Error creating wellbore:', error);
      throw error;
    }
  },

  getWellbores: async (params = {}) => {
    try {
      const response = await api.get('/wellbores', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching wellbores:', error);
      throw error;
    }
  },

  getWellboreById: async (wellboreId) => {
    try {
      const response = await api.get(`/wellbores/${wellboreId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching wellbore details:', error);
      throw error;
    }
  },

  updateWellbore: async (wellboreId, wellboreData) => {
    try {
      const response = await api.put(`/wellbores/${wellboreId}`, wellboreData);
      return response.data;
    } catch (error) {
      console.error('Error updating wellbore:', error);
      throw error;
    }
  },

  deleteWellbore: async (wellboreId) => {
    try {
      await api.delete(`/wellbores/${wellboreId}`);
      return true;
    } catch (error) {
      console.error('Error deleting wellbore:', error);
      throw error;
    }
  }
};

export default wellboreGeometryService;