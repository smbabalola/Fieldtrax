import api from './api';

const BASE_URL = '/trajectories';

const trajectoryService = {
  createTrajectory: async (trajectoryData) => {
    try {
      const response = await api.post(BASE_URL, trajectoryData);
      return response.data;
    } catch (error) {
      console.error('Error creating trajectory:', error);
      throw error;
    }
  },

  getTrajectories: async (params = {}) => {
    try {
      const response = await api.get(BASE_URL, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching trajectories:', error);
      throw error;
    }
  },

  getTrajectoryById: async (trajectoryId) => {
    try {
      const response = await api.get(`${BASE_URL}/${trajectoryId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching trajectory details:', error);
      throw error;
    }
  },

  updateTrajectory: async (trajectoryId, trajectoryData) => {
    try {
      const response = await api.put(`${BASE_URL}/${trajectoryId}`, trajectoryData);
      return response.data;
    } catch (error) {
      console.error('Error updating trajectory:', error);
      throw error;
    }
  },

  deleteTrajectory: async (trajectoryId) => {
    try {
      await api.delete(`${BASE_URL}/${trajectoryId}`);
      return true;
    } catch (error) {
      console.error('Error deleting trajectory:', error);
      throw error;
    }
  }
};

export default trajectoryService;