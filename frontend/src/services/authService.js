// File: /src/services/authService.js
import api from './api';

const authService = {
  /**
   * Verify authentication status
   * @returns {Promise<Object>} Authentication status
   */
  verifyAuth: async () => {
    try {
      const response = await api.post('/auth/verify');
      return response.data;
    } catch (error) {
      console.error('Error verifying authentication:', error);
      throw error;
    }
  },

  /**
   * Logout user
   * @returns {Promise<Object>} Logout response
   */
  logout: async () => {
    try {
      const response = await api.post('/auth/logout');
      return response.data;
    } catch (error) {
      console.error('Error logging out:', error);
      throw error;
    }
  },

  /**
   * Refresh access token
   * @param {string} refreshToken Refresh token
   * @returns {Promise<Object>} New session data
   */
  refreshToken: async (refreshToken) => {
    try {
      const response = await api.post('/auth/refresh', { refresh_token: refreshToken });
      return response.data;
    } catch (error) {
      console.error('Error refreshing token:', error);
      throw error;
    }
  },

  /**
   * Login user
   * @param {Object} loginData Login data
   * @returns {Promise<Object>} Session data
   */
  login: async (loginData) => {
    try {
      const response = await api.post('/auth/login', loginData);
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  }
};

export default authService;