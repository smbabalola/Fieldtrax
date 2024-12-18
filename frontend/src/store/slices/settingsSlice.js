// src/store/slices/settingsSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import settingsService from '../../services/settingsService';

// Default settings that will be used for reset
const defaultSettings = settingsService.defaults;

// Enhanced error handling for API calls
const handleServiceError = (error) => {
  console.warn('Settings service error:', error);
  return {
    message: error.message || 'An error occurred',
    code: error.code || 'UNKNOWN_ERROR',
    fallbackToDefaults: true
  };
};

// Async thunks
export const fetchSettings = createAsyncThunk(
  'settings/fetchSettings',
  async (_, { rejectWithValue }) => {
    try {
      const response = await settingsService.getSettings();
      return response.data;
    } catch (error) {
      return rejectWithValue(handleServiceError(error));
    }
  }
);

export const updateSettings = createAsyncThunk(
  'settings/updateSettings',
  async (settingsData, { rejectWithValue }) => {
    try {
      const response = await settingsService.updateSettings(settingsData);
      return response.data;
    } catch (error) {
      return rejectWithValue(handleServiceError(error));
    }
  }
);

export const resetSettings = createAsyncThunk(
  'settings/resetSettings',
  async (_, { rejectWithValue }) => {
    try {
      const response = await settingsService.resetSettings();
      return response.data;
    } catch (error) {
      return rejectWithValue(handleServiceError(error));
    }
  }
);

// Initial state
const initialState = {
  data: defaultSettings,
  isLoading: false,
  error: null,
  initialized: false,
  usingFallback: false
};

// Slice
const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    // Keep all existing reducers
    toggleSidebar: (state) => {
      state.data.display.sidebarOpen = !state.data.display.sidebarOpen;
    },
    setActiveJob: (state, action) => {
      state.data.activeJobId = action.payload;
    },
    clearActiveJob: (state) => {
      state.data.activeJobId = null;
    },
    setDisplaySettings: (state, action) => {
      state.data.display = {
        ...state.data.display,
        ...action.payload
      };
    },
    updateDisplaySettings: (state, action) => {
      state.data.display = {
        ...state.data.display,
        ...action.payload
      };
    },
    setTheme: (state, action) => {
      state.data.theme = {
        ...state.data.theme,
        ...action.payload
      };
    },
    updateTableSettings: (state, action) => {
      state.data.table = {
        ...state.data.table,
        ...action.payload
      };
    },
    resetToDefaults: (state) => {
      state.data = defaultSettings;
      state.usingFallback = false;
    },
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch settings
      .addCase(fetchSettings.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSettings.fulfilled, (state, action) => {
        state.isLoading = false;
        state.initialized = true;
        state.usingFallback = false;
        state.data = action.payload;
      })
      .addCase(fetchSettings.rejected, (state, action) => {
        state.isLoading = false;
        state.initialized = true;
        state.error = action.payload?.message || 'Failed to fetch settings';
        if (action.payload?.fallbackToDefaults) {
          state.data = defaultSettings;
          state.usingFallback = true;
        }
      })
      // Update settings
      .addCase(updateSettings.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateSettings.fulfilled, (state, action) => {
        state.isLoading = false;
        state.usingFallback = false;
        state.data = action.payload;
      })
      .addCase(updateSettings.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to update settings';
      })
      // Reset settings
      .addCase(resetSettings.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(resetSettings.fulfilled, (state, action) => {
        state.isLoading = false;
        state.usingFallback = false;
        state.data = action.payload;
      })
      .addCase(resetSettings.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload?.message || 'Failed to reset settings';
      });
  }
});

// Export all existing actions
export const {
  toggleSidebar,
  setActiveJob,
  clearActiveJob,
  setDisplaySettings,
  updateDisplaySettings,
  setTheme,
  updateTableSettings,
  resetToDefaults,
  clearError
} = settingsSlice.actions;

// Keep all existing selectors
export const selectSettings = (state) => state.settings.data;
export const selectIsLoading = (state) => state.settings.isLoading;
export const selectError = (state) => state.settings.error;
export const selectDisplaySettings = (state) => state.settings.data.display;
export const selectActiveJobId = (state) => state.settings.data.activeJobId;
export const selectTheme = (state) => state.settings.data.theme;
export const selectTableSettings = (state) => state.settings.data.table;
export const selectIsInitialized = (state) => state.settings.initialized;
export const selectIsUsingFallback = (state) => state.settings.usingFallback;

export default settingsSlice.reducer;