// src/store/slices/operatorSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import operatorService from '../../services/operatorService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchOperators = createAsyncThunk(
  'operators/fetchOperators',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `operators_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await operatorService.getAll(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchOperatorDetails = createAsyncThunk(
  'operators/fetchOperatorDetails',
  async (operatorId, { rejectWithValue }) => {
    try {
      const response = await operatorService.getByCode(operatorId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createOperator = createAsyncThunk(
  'operators/createOperator',
  async (operatorData, { rejectWithValue }) => {
    try {
      const response = await operatorService.create(operatorData);
      cacheService.clear(); // Invalidate cache after creation
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateOperator = createAsyncThunk(
  'operators/updateOperator',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await operatorService.update(id, data);
      cacheService.clear(); // Invalidate cache after update
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteOperator = createAsyncThunk(
  'operators/deleteOperator',
  async (operatorId, { rejectWithValue }) => {
    try {
      await operatorService.delete(operatorId);
      cacheService.clear(); // Invalidate cache after deletion
      return operatorId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Initial filters state
const initialFilters = {
  searchTerm: '',
  country: 'ALL',
  status: 'ALL',
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  operators: [],
  selectedOperator: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  operatorDetailsLoading: false,
  error: null,
  operatorDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'company_name',
    order: 'asc'
  },
  lastUpdated: null
};

// Slice
const operatorSlice = createSlice({
  name: 'operators',
  initialState,
  reducers: {
    clearOperatorDetails: (state) => {
      state.selectedOperator = null;
      state.operatorDetailsError = null;
    },
    setFilter: (state, action) => {
      state.filters = {
        ...state.filters,
        ...action.payload
      };
      // Reset to first page when filters change
      state.pagination.currentPage = 1;
    },
    resetFilters: (state) => {
      state.filters = initialFilters;
      state.pagination.currentPage = 1;
    },
    setSorting: (state, action) => {
      state.sorting = action.payload;
      // Reset to first page when sorting changes
      state.pagination.currentPage = 1;
    },
    setPage: (state, action) => {
      state.pagination.currentPage = action.payload;
    },
    setPageSize: (state, action) => {
      state.pagination.pageSize = action.payload;
      state.pagination.currentPage = 1; // Reset to first page when page size changes
    },
    clearErrors: (state) => {
      state.error = null;
      state.operatorDetailsError = null;
    },
    updateLastModified: (state) => {
      state.lastUpdated = new Date().toISOString();
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Operators
      .addCase(fetchOperators.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchOperators.fulfilled, (state, action) => {
        state.loading = false;
        state.operators = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchOperators.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch operators';
        state.operators = [];
      })

      // Fetch Operator Details
      .addCase(fetchOperatorDetails.pending, (state) => {
        state.operatorDetailsLoading = true;
        state.operatorDetailsError = null;
      })
      .addCase(fetchOperatorDetails.fulfilled, (state, action) => {
        state.operatorDetailsLoading = false;
        state.selectedOperator = action.payload;
        state.operatorDetailsError = null;
      })
      .addCase(fetchOperatorDetails.rejected, (state, action) => {
        state.operatorDetailsLoading = false;
        state.operatorDetailsError = action.payload;
      })

      // Create Operator
      .addCase(createOperator.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createOperator.fulfilled, (state, action) => {
        state.loading = false;
        state.operators.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createOperator.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Operator
      .addCase(updateOperator.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateOperator.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.operators.findIndex(op => op.id === action.payload.id);
        if (index !== -1) {
          state.operators[index] = action.payload;
        }
        if (state.selectedOperator?.id === action.payload.id) {
          state.selectedOperator = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateOperator.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Operator
      .addCase(deleteOperator.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteOperator.fulfilled, (state, action) => {
        state.loading = false;
        state.operators = state.operators.filter(op => op.id !== action.payload);
        if (state.selectedOperator?.id === action.payload) {
          state.selectedOperator = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteOperator.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// Action Creators
export const {
  clearOperatorDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateLastModified
} = operatorSlice.actions;

// Basic Selectors
export const selectOperators = state => state.operators.operators;
export const selectSelectedOperator = state => state.operators.selectedOperator;
export const selectLoading = state => state.operators.loading;
export const selectOperatorDetailsLoading = state => state.operators.operatorDetailsLoading;
export const selectError = state => state.operators.error;
export const selectOperatorDetailsError = state => state.operators.operatorDetailsError;
export const selectPagination = state => state.operators.pagination;
export const selectFilters = state => state.operators.filters;
export const selectSorting = state => state.operators.sorting;
export const selectLastUpdated = state => state.operators.lastUpdated;

// Complex Selectors
export const selectFilteredOperators = state => {
  const operators = selectOperators(state);
  const filters = selectFilters(state);
  
  return operators.filter(operator => {
    const matchesSearch = !filters.searchTerm || 
      operator.company_name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      operator.contact_name?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesCountry = filters.country === 'ALL' || operator.country === filters.country;
    
    const matchesStatus = filters.status === 'ALL' || operator.status === filters.status;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(operator.created_at) >= new Date(filters.dateRange.startDate) &&
       new Date(operator.created_at) <= new Date(filters.dateRange.endDate));

    return matchesSearch && matchesCountry && matchesStatus && matchesDateRange;
  });
};

export const selectOperatorById = (state, operatorId) => 
  state.operators.operators.find(operator => operator.id === operatorId);

export default operatorSlice.reducer;