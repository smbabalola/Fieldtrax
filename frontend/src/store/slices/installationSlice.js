// src/store/slices/installationSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import installationService from '../../services/installationService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchInstallations = createAsyncThunk(
  'installations/fetchInstallations',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `installations_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await installationService.getAll(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchInstallationsByField = createAsyncThunk(
  'installations/fetchInstallationsByField',
  async (fieldId, { rejectWithValue }) => {
    try {
      const response = await installationService.getByField(fieldId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchInstallationsByType = createAsyncThunk(
  'installations/fetchInstallationsByType',
  async (typeId, { rejectWithValue }) => {
    try {
      const response = await installationService.getByType(typeId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createInstallation = createAsyncThunk(
  'installations/createInstallation',
  async (installationData, { rejectWithValue }) => {
    try {
      const response = await installationService.create(installationData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateInstallation = createAsyncThunk(
  'installations/updateInstallation',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await installationService.update(id, data);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteInstallation = createAsyncThunk(
  'installations/deleteInstallation',
  async (id, { rejectWithValue }) => {
    try {
      await installationService.delete(id);
      cacheService.clear();
      return id;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  fieldId: null,
  type: null,
  country: null,
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  installations: [],
  selectedInstallation: null,
  installationTypes: [],
  slots: [],
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  installationDetailsLoading: false,
  error: null,
  installationDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'name',
    order: 'asc'
  },
  statistics: {
    totalInstallations: 0,
    activeInstallations: 0,
    totalSlots: 0,
    occupiedSlots: 0
  },
  lastUpdated: null
};

// Slice
const installationSlice = createSlice({
  name: 'installations',
  initialState,
  reducers: {
    clearInstallationDetails: (state) => {
      state.selectedInstallation = null;
      state.installationDetailsError = null;
    },
    setFilter: (state, action) => {
      state.filters = {
        ...state.filters,
        ...action.payload
      };
      state.pagination.currentPage = 1;
    },
    resetFilters: (state) => {
      state.filters = initialFilters;
      state.pagination.currentPage = 1;
    },
    setSorting: (state, action) => {
      state.sorting = action.payload;
      state.pagination.currentPage = 1;
    },
    setPage: (state, action) => {
      state.pagination.currentPage = action.payload;
    },
    setPageSize: (state, action) => {
      state.pagination.pageSize = action.payload;
      state.pagination.currentPage = 1;
    },
    clearErrors: (state) => {
      state.error = null;
      state.installationDetailsError = null;
    },
    updateStatistics: (state, action) => {
      state.statistics = {
        ...state.statistics,
        ...action.payload
      };
    },
    updateSlotStatus: (state, action) => {
      const { slotId, status } = action.payload;
      const slotIndex = state.slots.findIndex(slot => slot.id === slotId);
      if (slotIndex !== -1) {
        state.slots[slotIndex].status = status;
        state.statistics.occupiedSlots = state.slots.filter(slot => slot.status === 'OCCUPIED').length;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Installations
      .addCase(fetchInstallations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInstallations.fulfilled, (state, action) => {
        state.loading = false;
        state.installations = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchInstallations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch installations';
        state.installations = [];
      })

      // Fetch Installations By Field
      .addCase(fetchInstallationsByField.fulfilled, (state, action) => {
        state.installations = action.payload || [];
        state.lastUpdated = new Date().toISOString();
      })

      // Fetch Installations By Type
      .addCase(fetchInstallationsByType.fulfilled, (state, action) => {
        state.installations = action.payload || [];
        state.lastUpdated = new Date().toISOString();
      })

      // Create Installation
      .addCase(createInstallation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createInstallation.fulfilled, (state, action) => {
        state.loading = false;
        state.installations.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
        state.statistics.totalInstallations += 1;
      })
      .addCase(createInstallation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Installation
      .addCase(updateInstallation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateInstallation.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.installations.findIndex(i => i.id === action.payload.id);
        if (index !== -1) {
          state.installations[index] = action.payload;
        }
        if (state.selectedInstallation?.id === action.payload.id) {
          state.selectedInstallation = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateInstallation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Installation
      .addCase(deleteInstallation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteInstallation.fulfilled, (state, action) => {
        state.loading = false;
        state.installations = state.installations.filter(i => i.id !== action.payload);
        if (state.selectedInstallation?.id === action.payload) {
          state.selectedInstallation = null;
        }
        state.pagination.totalItems -= 1;
        state.statistics.totalInstallations -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteInstallation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// Action Creators
export const {
  clearInstallationDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateStatistics,
  updateSlotStatus
} = installationSlice.actions;

// Basic Selectors
export const selectInstallations = state => state.installations.installations;
export const selectSelectedInstallation = state => state.installations.selectedInstallation;
export const selectInstallationTypes = state => state.installations.installationTypes;
export const selectSlots = state => state.installations.slots;
export const selectLoading = state => state.installations.loading;
export const selectError = state => state.installations.error;
export const selectPagination = state => state.installations.pagination;
export const selectFilters = state => state.installations.filters;
export const selectSorting = state => state.installations.sorting;
export const selectStatistics = state => state.installations.statistics;
export const selectLastUpdated = state => state.installations.lastUpdated;

// Complex Selectors
export const selectFilteredInstallations = state => {
  const installations = selectInstallations(state);
  const filters = selectFilters(state);
  
  return installations.filter(installation => {
    const matchesStatus = filters.status === 'ALL' || installation.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      installation.name?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesField = !filters.fieldId || installation.field_id === filters.fieldId;
    const matchesType = !filters.type || installation.type === filters.type;
    const matchesCountry = !filters.country || installation.country === filters.country;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(installation.commissioned_date) >= new Date(filters.dateRange.startDate) &&
       new Date(installation.commissioned_date) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesSearch && matchesField && 
           matchesType && matchesCountry && matchesDateRange;
  });
};

export const selectInstallationById = (state, installationId) => 
  state.installations.installations.find(installation => installation.id === installationId);

export const selectActiveInstallations = state =>
  state.installations.installations.filter(installation => installation.status === 'ACTIVE');

export const selectAvailableSlots = state =>
  state.installations.slots.filter(slot => slot.status === 'AVAILABLE');

export const selectOccupiedSlots = state =>
  state.installations.slots.filter(slot => slot.status === 'OCCUPIED');

export default installationSlice.reducer;