import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import authService from '../../services/authService';

// Async thunks
export const fetchDashboardData = createAsyncThunk(
  'dashboard/fetchData',
  async (_, { rejectWithValue }) => {
    try {
      const [settings, stats] = await Promise.all([
        authService.getUserSettings(),
        authService.getDashboardStats()
      ]);
      return { settings, stats };
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || error.message);
    }
  }
);

const initialState = {
  isLoading: false,
  error: null,
  settings: {
    sidebarOpen: true,
    theme: 'light',
    activeJobId: null,
    displayMode: 'grid',
    defaultView: 'jobs',
    notifications: {
      enabled: true,
      sound: true,
    }
  },
  stats: {
    activeJobs: 0,
    completedJobs: 0,
    totalWells: 0,
    activeOperations: 0
  },
  lastSync: null
};

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.settings.sidebarOpen = !state.settings.sidebarOpen;
    },
    updateSettings: (state, action) => {
      state.settings = {
        ...state.settings,
        ...action.payload
      };
    },
    setTheme: (state, action) => {
      state.settings.theme = action.payload;
    },
    setActiveJob: (state, action) => {
      state.settings.activeJobId = action.payload;
    },
    setDisplayMode: (state, action) => {
      state.settings.displayMode = action.payload;
    },
    toggleNotifications: (state, action) => {
      state.settings.notifications = {
        ...state.settings.notifications,
        ...action.payload
      };
    },
    resetDashboard: () => initialState,
    clearError: (state) => {
      state.error = null;
    },
    updateLastSync: (state) => {
      state.lastSync = new Date().toISOString();
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.settings = {
          ...state.settings,
          ...action.payload.settings
        };
        state.stats = action.payload.stats;
        state.lastSync = new Date().toISOString();
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  }
});

// Selectors
export const selectDashboardSettings = (state) => state.dashboard.settings;
export const selectDashboardStats = (state) => state.dashboard.stats;
export const selectDashboardLoading = (state) => state.dashboard.isLoading;
export const selectDashboardError = (state) => state.dashboard.error;
export const selectLastSync = (state) => state.dashboard.lastSync;
export const selectActiveJobId = (state) => state.dashboard.settings.activeJobId;

export const {
  toggleSidebar,
  updateSettings,
  setTheme,
  setActiveJob,
  setDisplayMode,
  toggleNotifications,
  resetDashboard,
  clearError,
  updateLastSync
} = dashboardSlice.actions;

export default dashboardSlice.reducer;