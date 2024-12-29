// src/services/settingsService.js
import api from '../services/api';

const SETTINGS_BASE_URL = '/settings';

const defaultSettings = {
  display: {
    sidebarOpen: true,
    density: 'comfortable',
    fontSize: 'medium',
    showGridLines: true
  },
  theme: {
    mode: 'light',
    primary: '#007bff',
    secondary: '#6c757d'
  },
  activeJobId: null,
  dateFormat: 'MM/DD/YYYY',
  timeFormat: '12h',
  language: 'en',
  notifications: {
    email: true,
    push: true,
    sms: false
  },
  table: {
    rowsPerPage: 10,
    sortDirection: 'asc'
  }
};

const getStoredSettings = () => {
  try {
    const stored = localStorage.getItem('settings');
    if (!stored) return null;
    const parsed = JSON.parse(stored);
    return typeof parsed === 'object' ? parsed : null;
  } catch (error) {
    console.warn('Failed to parse stored settings:', error);
    return null;
  }
};

const storeSettings = (settings) => {
  try {
    localStorage.setItem('settings', JSON.stringify(settings));
    return true;
  } catch (error) {
    console.warn('Failed to store settings:', error);
    return false;
  }
};

const settingsService = {
  defaults: defaultSettings,

  getSettings: async () => {
    try {
      const response = await api.get(SETTINGS_BASE_URL);
      return response.data;
    } catch (error) {
      console.warn('Settings API error:', error);
      return null;
    }
  },

  updateSettings: async (settingsData) => {
    try {
      const response = await api.put(SETTINGS_BASE_URL, settingsData);
      return response.data;
    } catch (error) {
      console.warn('Error updating settings:', error);
      return null;
    }
  },

  resetSettings: async () => {
    try {
      const response = await api.post(`${SETTINGS_BASE_URL}/reset`);
      return response.data;
    } catch (error) {
      console.warn('Failed to reset settings on server:', error);
      return null;
    }
  },

  getInitialSettings: () => {
    const storedSettings = getStoredSettings();
    return {
      ...defaultSettings,
      ...(storedSettings || {}),
      _source: storedSettings ? 'cache' : 'defaults'
    };
  },

  /**
   * Get user-specific settings
   * @param {string} userId User ID
   * @returns {Promise<Object>} User settings
   */
  getUserSettings: async (userId) => {
    try {
      const response = await api.get(`${SETTINGS_BASE_URL}/user/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user settings:', error);
      throw error;
    }
  },

  /**
   * Update user-specific settings
   * @param {string} userId User ID
   * @param {Object} settingsData Settings data to update
   * @returns {Promise<Object>} Updated settings
   */
  updateUserSettings: async (userId, settingsData) => {
    try {
      const response = await api.put(`${SETTINGS_BASE_URL}/user/${userId}`, settingsData);
      return response.data;
    } catch (error) {
      console.error('Error updating user settings:', error);
      throw error;
    }
  }
};

export default settingsService;