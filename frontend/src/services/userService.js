import api, { API_ENDPOINTS, handleApiError } from './api';

const userService = {
  /**
   * Create a new user
   * @param {Object} userData User data
   * @returns {Promise<Object>} Created user data
   */
  createUser: async (userData) => {
    try {
      const response = await api.post(API_ENDPOINTS.users.create, userData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error creating user');
    }
  },

  /**
   * Get current user details
   * @returns {Promise<Object>} Current user data
   */
  getCurrentUser: async () => {
    try {
      const response = await api.get(API_ENDPOINTS.users.me);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching current user details');
    }
  },

  /**
   * Update current user details
   * @param {Object} userData Updated user data
   * @returns {Promise<Object>} Updated user data
   */
  updateCurrentUser: async (userData) => {
    try {
      const response = await api.put(API_ENDPOINTS.users.me, userData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating current user details');
    }
  },

  /**
   * Verify user email
   * @param {string} token Verification token
   * @returns {Promise<Object>} Verification response
   */
  verifyEmail: async (token) => {
    try {
      const response = await api.post(API_ENDPOINTS.users.verifyEmail, { token });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error verifying email');
    }
  },

  /**
   * Send verification email
   * @returns {Promise<Object>} Response from sending verification email
   */
  sendVerificationEmail: async () => {
    try {
      const response = await api.post(API_ENDPOINTS.users.sendVerification);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error sending verification email');
    }
  },

  /**
   * Change user password
   * @param {string} currentPassword Current password
   * @param {string} newPassword New password
   * @returns {Promise<Object>} Response from changing password
   */
  changePassword: async (currentPassword, newPassword) => {
    try {
      const response = await api.post(API_ENDPOINTS.users.changePassword, {
        current_password: currentPassword,
        new_password: newPassword
      });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error changing password');
    }
  },

  /**
   * Get users
   * @param {Object} params Query parameters
   * @returns {Promise<Object>} List of users
   */
  getUsers: async (params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.users.list, { params });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching users');
    }
  },

  /**
   * Get user by ID
   * @param {string} userId User ID
   * @returns {Promise<Object>} User data
   */
  getUserById: async (userId) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.users.details}/${userId}`);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching user details');
    }
  },

  /**
   * Update user by ID
   * @param {string} userId User ID
   * @param {Object} userData Updated user data
   * @returns {Promise<Object>} Updated user data
   */
  updateUser: async (userId, userData) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.users.details}/${userId}`, userData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating user');
    }
  },

  /**
   * Delete user by ID
   * @param {string} userId User ID
   * @returns {Promise<boolean>} Deletion status
   */
  deleteUser: async (userId) => {
    try {
      await api.delete(`${API_ENDPOINTS.users.details}/${userId}`);
      return true;
    } catch (error) {
      return handleApiError(error, 'Error deleting user');
    }
  }
};

export default userService;
