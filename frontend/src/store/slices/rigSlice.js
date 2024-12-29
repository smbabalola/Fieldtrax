// src/store/slices/rigSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import rigService from '../../services/rigService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchRigs = createAsyncThunk(
  'rigs/fetchRigs',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `rigs_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await rigService.getAllRigs(params);
      cacheService.set(cacheKey, response);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchActiveRigs = createAsyncThunk(
  'rigs/fetchActiveRigs',
  async (_, { rejectWithValue }) => {
    try {
      const cacheKey = 'active_rigs';
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await rigService.getActiveRigs();
      cacheService.set(cacheKey, response);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchRigById = createAsyncThunk(
  'rigs/fetchRigById',
  async (rigId, { rejectWithValue }) => {
    try {
      const response = await rigService.getRigById(rigId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createRig = createAsyncThunk(
  'rigs/createRig',
  async (rigData, { rejectWithValue }) => {
    try {
      const validation = rigService.validateRigData(rigData);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await rigService.createRig(rigData);
      cacheService.clear(); // Invalidate cache after creation
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateRig = createAsyncThunk(
  'rigs/updateRig',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const validation = rigService.validateRigData(data);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await rigService.updateRig(id, data);
      cacheService.clear(); // Invalidate cache after update
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteRig = createAsyncThunk(
  'rigs/deleteRig',
  async (rigId, { rejectWithValue }) => {
    try {
      await rigService.deleteRig(rigId);
      cacheService.clear(); // Invalidate cache after deletion
      return rigId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Initial State
const initialState = {
  rigs: [],
  activeRigs: [],
  selectedRig: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  rigDetailsLoading: false,
  error: null,
  rigDetailsError: null,
  filters: {
    status: 'ALL',
    searchTerm: '',
    contractor: null,
    dateRange: {
      startDate: null,
      endDate: null
    }
  },
  sorting: {
    field: 'created_at',
    order: 'desc'
  }
};

// Slice
const rigSlice = createSlice({
  name: 'rigs',
  initialState,
  reducers: {
    clearRigDetails: (state) => {
      state.selectedRig = null;
      state.rigDetailsError = null;
    },
    setFilter: (state, action) => {
      state.filters = {
        ...state.filters,
        ...action.payload
      };
      state.pagination.currentPage = 1;
    },
    resetFilters: (state) => {
      state.filters = initialState.filters;
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
      state.rigDetailsError = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Rigs
      .addCase(fetchRigs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRigs.fulfilled, (state, action) => {
        state.loading = false;
        state.rigs = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.error = null;
      })
      .addCase(fetchRigs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch rigs';
        state.rigs = [];
      })

      // Fetch Active Rigs
      .addCase(fetchActiveRigs.fulfilled, (state, action) => {
        state.activeRigs = action.payload || [];
      })

      // Fetch Rig Details
      .addCase(fetchRigById.pending, (state) => {
        state.rigDetailsLoading = true;
        state.rigDetailsError = null;
      })
      .addCase(fetchRigById.fulfilled, (state, action) => {
        state.rigDetailsLoading = false;
        state.selectedRig = action.payload;
        state.rigDetailsError = null;
      })
      .addCase(fetchRigById.rejected, (state, action) => {
        state.rigDetailsLoading = false;
        state.rigDetailsError = action.payload;
      })

      // Create Rig
      .addCase(createRig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createRig.fulfilled, (state, action) => {
        state.loading = false;
        state.rigs.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.error = null;
      })
      .addCase(createRig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Rig
      .addCase(updateRig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateRig.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.rigs.findIndex(rig => rig.id === action.payload.id);
        if (index !== -1) {
          state.rigs[index] = action.payload;
        }
        if (state.selectedRig?.id === action.payload.id) {
          state.selectedRig = action.payload;
        }
        state.error = null;
      })
      .addCase(updateRig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Rig
      .addCase(deleteRig.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteRig.fulfilled, (state, action) => {
        state.loading = false;
        state.rigs = state.rigs.filter(rig => rig.id !== action.payload);
        if (state.selectedRig?.id === action.payload) {
          state.selectedRig = null;
        }
        state.pagination.totalItems -= 1;
        state.error = null;
      })
      .addCase(deleteRig.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// Action Creators
export const {
  clearRigDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors
} = rigSlice.actions;

// Basic Selectors
export const selectRigs = state => state.rigs.rigs;
export const selectActiveRigs = state => state.rigs.activeRigs;
export const selectSelectedRig = state => state.rigs.selectedRig;
export const selectRigDetailsLoading = state => state.rigs.rigDetailsLoading;
export const selectRigDetailsError = state => state.rigs.rigDetailsError;
export const selectLoading = state => state.rigs.loading;
export const selectError = state => state.rigs.error;
export const selectFilters = state => state.rigs.filters;
export const selectPagination = state => state.rigs.pagination;
export const selectSorting = state => state.rigs.sorting;

// Complex Selectors
export const selectFilteredRigs = state => {
  const rigs = selectRigs(state);
  const filters = selectFilters(state);
  
  return rigs.filter(rig => {
    const matchesStatus = filters.status === 'ALL' || rig.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      rig.rig_name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      rig.rig_number?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesContractor = !filters.contractor || rig.contractor_id === filters.contractor;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(rig.created_at) >= new Date(filters.dateRange.startDate) &&
       new Date(rig.created_at) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesSearch && matchesContractor && matchesDateRange;
  });
};

export const selectRigById = (state, rigId) => 
  state.rigs.rigs.find(rig => rig.id === rigId);

export default rigSlice.reducer;