// src/services/settingsService.js
import apiRequest from '../utils/apiUtils';

// Remove the /api/v1 prefix since it's in the baseURL
const SETTINGS_BASE_URL = '/settings';

// Default settings configuration
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

// Helper to safely get stored settings
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

// Helper to safely store settings
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
  // Expose default settings
  defaults: defaultSettings,

  // Get all settings
  getSettings: async () => {
    try {
      // First try to get from local storage
      const storedSettings = getStoredSettings();
      
      // Then try to get from API
      const response = await apiRequest.get(SETTINGS_BASE_URL);
      const serverSettings = response.data || {};
      
      // Merge settings in priority order: defaults < stored < server
      const mergedSettings = {
        ...defaultSettings,
        ...(storedSettings || {}),
        ...serverSettings
      };

      // Store the merged settings
      storeSettings(mergedSettings);
      
      return { data: mergedSettings };
    } catch (error) {
      console.warn('Settings API error:', error);
      
      // If API fails, try to use stored settings
      const storedSettings = getStoredSettings();
      if (storedSettings) {
        console.log('Using stored settings due to API error');
        return {
          data: {
            ...defaultSettings,
            ...storedSettings,
            _source: 'cache'
          }
        };
      }

      // If no stored settings, use defaults
      console.log('Using default settings');
      return {
        data: {
          ...defaultSettings,
          _source: 'defaults'
        }
      };
    }
  },

  // Update settings
  updateSettings: async (settingsData) => {
    try {
      // Validate input
      if (!settingsData || typeof settingsData !== 'object') {
        throw new Error('Invalid settings data');
      }

      // Send to API
      const response = await apiRequest.put(SETTINGS_BASE_URL, settingsData);
      const updatedSettings = response.data || {};
      
      // Merge with defaults and store
      const mergedSettings = {
        ...defaultSettings,
        ...updatedSettings
      };
      storeSettings(mergedSettings);
      
      return { data: mergedSettings };
    } catch (error) {
      console.error('Failed to update settings:', error);
      throw error;
    }
  },

  // Reset settings
  resetSettings: async () => {
    try {
      // Call reset endpoint
      await apiRequest.post(`${SETTINGS_BASE_URL}/reset`);
      
      // Clear stored settings
      localStorage.removeItem('settings');
      
      return { data: defaultSettings };
    } catch (error) {
      console.warn('Failed to reset settings on server:', error);
      
      // Even if API fails, clear local storage and return defaults
      localStorage.removeItem('settings');
      return {
        data: {
          ...defaultSettings,
          _source: 'defaults'
        }
      };
    }
  },

  // Get initial settings (for app bootstrap)
  getInitialSettings: () => {
    const storedSettings = getStoredSettings();
    return {
      data: {
        ...defaultSettings,
        ...(storedSettings || {}),
        _source: storedSettings ? 'cache' : 'defaults'
      }
    };
  }
};

export default settingsService;