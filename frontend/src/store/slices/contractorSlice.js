// src/store/slices/contractorSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import contractorService from '../../services/contractorService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchContractors = createAsyncThunk(
  'contractors/fetchContractors',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `contractors_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await contractorService.getAll(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchContractorsByName = createAsyncThunk(
  'contractors/fetchContractorsByName',
  async (name, { rejectWithValue }) => {
    try {
      const response = await contractorService.getByName(name);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchContractorsByCountry = createAsyncThunk(
  'contractors/fetchContractorsByCountry',
  async (country, { rejectWithValue }) => {
    try {
      const response = await contractorService.getByCountry(country);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createContractor = createAsyncThunk(
  'contractors/createContractor',
  async (contractorData, { rejectWithValue }) => {
    try {
      const response = await contractorService.create(contractorData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateContractor = createAsyncThunk(
  'contractors/updateContractor',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await contractorService.update(id, data);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteContractor = createAsyncThunk(
  'contractors/deleteContractor',
  async (contractorId, { rejectWithValue }) => {
    try {
      await contractorService.delete(contractorId);
      cacheService.clear();
      return contractorId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  country: null,
  type: null,
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  contractors: [],
  selectedContractor: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  contractorDetailsLoading: false,
  error: null,
  contractorDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'company_name',
    order: 'asc'
  },
  statistics: {
    totalContractors: 0,
    activeContracts: 0,
    totalRigs: 0
  },
  lastUpdated: null
};

// Slice
const contractorSlice = createSlice({
  name: 'contractors',
  initialState,
  reducers: {
    clearContractorDetails: (state) => {
      state.selectedContractor = null;
      state.contractorDetailsError = null;
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
      state.contractorDetailsError = null;
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
      // Fetch Contractors
      .addCase(fetchContractors.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchContractors.fulfilled, (state, action) => {
        state.loading = false;
        state.contractors = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchContractors.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch contractors';
        state.contractors = [];
      })

      // Fetch Contractors By Name
      .addCase(fetchContractorsByName.fulfilled, (state, action) => {
        state.contractors = action.payload;
        state.lastUpdated = new Date().toISOString();
      })

      // Fetch Contractors By Country
      .addCase(fetchContractorsByCountry.fulfilled, (state, action) => {
        state.contractors = action.payload;
        state.lastUpdated = new Date().toISOString();
      })

      // Create Contractor
      .addCase(createContractor.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createContractor.fulfilled, (state, action) => {
        state.loading = false;
        state.contractors.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createContractor.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Contractor
      .addCase(updateContractor.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateContractor.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.contractors.findIndex(c => c.id === action.payload.id);
        if (index !== -1) {
          state.contractors[index] = action.payload;
        }
        if (state.selectedContractor?.id === action.payload.id) {
          state.selectedContractor = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateContractor.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Contractor
      .addCase(deleteContractor.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteContractor.fulfilled, (state, action) => {
        state.loading = false;
        state.contractors = state.contractors.filter(c => c.id !== action.payload);
        if (state.selectedContractor?.id === action.payload) {
          state.selectedContractor = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteContractor.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// Action Creators
export const {
  clearContractorDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateStatistics
} = contractorSlice.actions;

// Basic Selectors
export const selectContractors = state => state.contractors.contractors;
export const selectSelectedContractor = state => state.contractors.selectedContractor;
export const selectLoading = state => state.contractors.loading;
export const selectError = state => state.contractors.error;
export const selectPagination = state => state.contractors.pagination;
export const selectFilters = state => state.contractors.filters;
export const selectSorting = state => state.contractors.sorting;
export const selectStatistics = state => state.contractors.statistics;
export const selectLastUpdated = state => state.contractors.lastUpdated;

// Complex Selectors
export const selectFilteredContractors = state => {
  const contractors = selectContractors(state);
  const filters = selectFilters(state);
  
  return contractors.filter(contractor => {
    const matchesStatus = filters.status === 'ALL' || contractor.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      contractor.company_name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      contractor.contact_name?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesCountry = !filters.country || contractor.country === filters.country;
    const matchesType = !filters.type || contractor.contractor_type === filters.type;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(contractor.contract_start) >= new Date(filters.dateRange.startDate) &&
       new Date(contractor.contract_end) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesSearch && matchesCountry && matchesType && matchesDateRange;
  });
};

export const selectContractorById = (state, contractorId) => 
  state.contractors.contractors.find(contractor => contractor.id === contractorId);

export const selectActiveContractors = state =>
  state.contractors.contractors.filter(contractor => contractor.status === 'ACTIVE');

export default contractorSlice.reducer;