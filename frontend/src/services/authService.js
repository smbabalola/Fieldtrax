// File: /frontend/src/services/authService.js
import { apiRequest } from '../utils/apiUtils';

const authService = {
  login: async (credentials) => {
    try {
      const response = await apiRequest('POST', '/login', credentials);
      if (response.token) {
        localStorage.setItem('user', JSON.stringify(response));
        localStorage.setItem('token', response.token);
      }
      return response;
    } catch (error) {
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = '/login';
  },

  getCurrentUser: () => {
    try {
      const userStr = localStorage.getItem('user');
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error('Error parsing user data:', error);
      localStorage.removeItem('user');
      return null;
    }
  },

  isAuthenticated: () => {
    const user = authService.getCurrentUser();
    return !!user;
  }
};

export default authService;