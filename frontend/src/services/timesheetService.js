
// File: /frontend/src/services/timeSheetService.js
import axios from 'axios';
import { handleApiError } from '../utils/errorHandler';

const API_URL = 'http://localhost:8000/api/v1';

const timeSheetService = {
  getTimeSheets: async (jobId) => {
    try {
      const response = await axios.get(`${API_URL}/time-sheets/job/${jobId}`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  getPendingTimeSheets: async () => {
    try {
      const response = await axios.get(`${API_URL}/time-sheets/pending`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  createTimeSheet: async (timeSheetData) => {
    try {
      const response = await axios.post(`${API_URL}/time-sheets/`, timeSheetData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  approveTimeSheet: async (timeSheetId) => {
    try {
      const response = await axios.post(`${API_URL}/time-sheets/${timeSheetId}/approve`);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },

  updateTimeSheet: async (timeSheetId, timeSheetData) => {
    try {
      const response = await axios.put(`${API_URL}/time-sheets/${timeSheetId}`, timeSheetData);
      return response.data;
    } catch (error) {
      throw handleApiError(error);
    }
  },
};

export default timeSheetService;