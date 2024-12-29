import api, { API_ENDPOINTS, handleApiError } from './api';

const roleService = {
  /**
   * Create a new role
   * @param {Object} roleData Role data
   * @returns {Promise<Object>} Created role data
   */
  createRole: async (roleData) => {
    try {
      const response = await api.post(API_ENDPOINTS.roles.create, roleData);
      return response.data;
    } catch (error) {
      console.error('Error creating role:', error);
      throw error;
    }
  },

  /**
   * Get all roles
   * @param {Object} params Query parameters
   * @returns {Promise<Array>} List of roles
   */
  getRoles: async (params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.roles.getAll, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching roles:', error);
      throw error;
    }
  },

  /**
   * Update a role
   * @param {string} roleId Role ID
   * @param {Object} roleData Updated role data
   * @returns {Promise<Object>} Updated role data
   */
  updateRole: async (roleId, roleData) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.roles.base}/${roleId}`, roleData);
      return response.data;
    } catch (error) {
      console.error('Error updating role:', error);
      throw error;
    }
  },

  /**
   * Delete a role
   * @param {string} roleId Role ID
   * @returns {Promise<void>}
   */
  deleteRole: async (roleId) => {
    try {
      await api.delete(`${API_ENDPOINTS.roles.base}/${roleId}`);
    } catch (error) {
      console.error('Error deleting role:', error);
      throw error;
    }
  },

  /**
   * Assign a role to a user
   * @param {string} userId User ID
   * @param {string} roleId Role ID
   * @returns {Promise<Object>} Response data
   */
  assignRoleToUser: async (userId, roleId) => {
    const response = await api.post(`/roles/users/${userId}/roles/${roleId}`);
    return response.data;
  },

  /**
   * Remove a role from a user
   * @param {string} userId User ID
   * @param {string} roleId Role ID
   * @returns {Promise<Object>} Response data
   */
  removeRoleFromUser: async (userId, roleId) => {
    const response = await api.delete(`/roles/users/${userId}/roles/${roleId}`);
    return response.data;
  },

  /**
   * Add a permission to a role
   * @param {string} roleId Role ID
   * @param {string} permissionId Permission ID
   * @returns {Promise<Object>} Response data
   */
  addPermissionToRole: async (roleId, permissionId) => {
    const response = await api.post(`/roles/${roleId}/permissions/${permissionId}`);
    return response.data;
  },

  /**
   * Remove a permission from a role
   * @param {string} roleId Role ID
   * @param {string} permissionId Permission ID
   * @returns {Promise<Object>} Response data
   */
  removePermissionFromRole: async (roleId, permissionId) => {
    const response = await api.delete(`/roles/${roleId}/permissions/${permissionId}`);
    return response.data;
  }
};

export default roleService;
