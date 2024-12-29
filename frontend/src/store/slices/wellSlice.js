// src/store/slices/wellSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import wellService from '../../services/wellService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchWells = createAsyncThunk(
  'wells/fetchWells',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `wells_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await wellService.getAllWells(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchWellById = createAsyncThunk(
  'wells/fetchWellById',
  async (wellId, { rejectWithValue }) => {
    try {
      const response = await wellService.getWellById(wellId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchWellsByOperator = createAsyncThunk(
  'wells/fetchWellsByOperator',
  async (operatorId, { rejectWithValue }) => {
    try {
      const response = await wellService.getWellsByOperator(operatorId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createWell = createAsyncThunk(
  'wells/createWell',
  async (wellData, { rejectWithValue }) => {
    try {
      const validation = wellService.validateWellData(wellData);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await wellService.createWell(wellData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateWell = createAsyncThunk(
  'wells/updateWell',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const validation = wellService.validateWellData(data);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await wellService.updateWell(id, data);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteWell = createAsyncThunk(
  'wells/deleteWell',
  async (wellId, { rejectWithValue }) => {
    try {
      await wellService.deleteWell(wellId);
      cacheService.clear();
      return wellId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchWellShapes = createAsyncThunk(
  'wells/fetchWellShapes',
  async (_, { rejectWithValue }) => {
    try {
      const response = await wellService.getWellShapes();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchWellTypes = createAsyncThunk(
  'wells/fetchWellTypes',
  async (_, { rejectWithValue }) => {
    try {
      const response = await wellService.getWellTypes();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  operatorId: null,
  wellType: null,
  field: null,
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  wells: [],
  selectedWell: null,
  wellShapes: [],
  wellTypes: [],
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  wellDetailsLoading: false,
  error: null,
  wellDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'well_name',
    order: 'asc'
  },
  relatedData: {
    loading: false,
    error: null
  },
  statistics: {
    totalWells: 0,
    activeWells: 0,
    completedWells: 0,
    suspendedWells: 0
  },
  lastUpdated: null
};

// Slice
const wellSlice = createSlice({
  name: 'wells',
  initialState,
  reducers: {
    clearWellDetails: (state) => {
      state.selectedWell = null;
      state.wellDetailsError = null;
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
      state.wellDetailsError = null;
    },
    updateStatistics: (state, action) => {
      state.statistics = {
        ...state.statistics,
        ...action.payload
      };
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Wells
      .addCase(fetchWells.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWells.fulfilled, (state, action) => {
        state.loading = false;
        state.wells = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchWells.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch wells';
        state.wells = [];
      })

      // Fetch Well Details
      .addCase(fetchWellById.pending, (state) => {
        state.wellDetailsLoading = true;
        state.wellDetailsError = null;
      })
      .addCase(fetchWellById.fulfilled, (state, action) => {
        state.wellDetailsLoading = false;
        state.selectedWell = action.payload;
        state.wellDetailsError = null;
      })
      .addCase(fetchWellById.rejected, (state, action) => {
        state.wellDetailsLoading = false;
        state.wellDetailsError = action.payload;
      })

      // Fetch Wells By Operator
      .addCase(fetchWellsByOperator.fulfilled, (state, action) => {
        state.wells = action.payload;
        state.lastUpdated = new Date().toISOString();
      })

      // Create Well
      .addCase(createWell.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createWell.fulfilled, (state, action) => {
        state.loading = false;
        state.wells.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createWell.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Well
      .addCase(updateWell.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateWell.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.wells.findIndex(well => well.id === action.payload.id);
        if (index !== -1) {
          state.wells[index] = action.payload;
        }
        if (state.selectedWell?.id === action.payload.id) {
          state.selectedWell = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateWell.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Well
      .addCase(deleteWell.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteWell.fulfilled, (state, action) => {
        state.loading = false;
        state.wells = state.wells.filter(well => well.id !== action.payload);
        if (state.selectedWell?.id === action.payload) {
          state.selectedWell = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteWell.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Fetch Well Shapes
      .addCase(fetchWellShapes.fulfilled, (state, action) => {
        state.wellShapes = action.payload || [];
      })

      // Fetch Well Types
      .addCase(fetchWellTypes.fulfilled, (state, action) => {
        state.wellTypes = action.payload || [];
      });
  }
});

// Action Creators
export const {
  clearWellDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateStatistics
} = wellSlice.actions;

// Basic Selectors
export const selectWells = state => state.wells.wells;
export const selectSelectedWell = state => state.wells.selectedWell;
export const selectWellShapes = state => state.wells.wellShapes;
export const selectWellTypes = state => state.wells.wellTypes;
export const selectLoading = state => state.wells.loading;
export const selectWellDetailsLoading = state => state.wells.wellDetailsLoading;
export const selectError = state => state.wells.error;
export const selectWellDetailsError = state => state.wells.wellDetailsError;
export const selectPagination = state => state.wells.pagination;
export const selectFilters = state => state.wells.filters;
export const selectSorting = state => state.wells.sorting;
export const selectStatistics = state => state.wells.statistics;
export const selectLastUpdated = state => state.wells.lastUpdated;

// Complex Selectors
export const selectFilteredWells = state => {
  const wells = selectWells(state);
  const filters = selectFilters(state);
  
  return wells.filter(well => {
    const matchesStatus = filters.status === 'ALL' || well.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      well.well_name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      well.api_number?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesOperator = !filters.operatorId || well.operator_id === filters.operatorId;
    const matchesWellType = !filters.wellType || well.well_type === filters.wellType;
    const matchesField = !filters.field || well.field === filters.field;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(well.spud_date) >= new Date(filters.dateRange.startDate) &&
       new Date(well.spud_date) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesSearch && matchesOperator && 
           matchesWellType && matchesField && matchesDateRange;
  });
};

export const selectWellById = (state, wellId) => 
  state.wells.wells.find(well => well.id === wellId);

export const selectWellsByOperator = (state, operatorId) =>
  state.wells.wells.filter(well => well.operator_id === operatorId);

export default wellSlice.reducer;