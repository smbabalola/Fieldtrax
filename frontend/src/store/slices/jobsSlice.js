// jobsSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import jobService from '../../services/jobService';

// Async Thunks
export const fetchJobs = createAsyncThunk(
  'jobs/fetchJobs',
  async (params, { rejectWithValue }) => {
    try {
      const response = await jobService.getJobs(params);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchJobDetails = createAsyncThunk(
  'jobs/fetchJobDetails',
  async (jobId, { rejectWithValue }) => {
    try {
      const response = await jobService.getById(jobId);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createJob = createAsyncThunk(
  'jobs/createJob',
  async (jobData, { rejectWithValue }) => {
    try {
      const response = await jobService.create(jobData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateJob = createAsyncThunk(
  'jobs/updateJob',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await jobService.update(id, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteJob = createAsyncThunk(
  'jobs/deleteJob',
  async (jobId, { rejectWithValue }) => {
    try {
      await jobService.delete(jobId);
      return jobId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchRelatedData = createAsyncThunk(
  'jobs/fetchRelatedData',
  async (_, { rejectWithValue }) => {
    try {
      const [rigs, wells, operators, purchaseOrders] = await Promise.all([
        jobService.getAll('rigs'),
        jobService.getAll('wells'),
        jobService.getAll('operators'),
        jobService.getAll('purchaseOrders')
      ]);
      
      return {
        rigs: rigs.data,
        wells: wells.data,
        operators: operators.data,
        purchaseOrders: purchaseOrders.data
      };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateJobStatus = createAsyncThunk(
  'jobs/updateJobStatus',
  async ({ jobId, status }, { rejectWithValue }) => {
    try {
      const response = await jobService.update(jobId, { status });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  jobs: [],
  selectedJob: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  jobDetailsLoading: false,
  error: null,
  jobDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'created_at',
    order: 'desc'
  },
  relatedData: {
    rigs: [],
    wells: [],
    operators: [],
    purchaseOrders: [],
    loading: false,
    error: null
  }
};

// Slice
const jobsSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    clearJobDetails: (state) => {
      state.selectedJob = null;
      state.jobDetailsError = null;
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
      state.jobDetailsError = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Jobs
      .addCase(fetchJobs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJobs.fulfilled, (state, action) => {
        state.loading = false;
        const response = action.payload;
        
        // Always set jobs array, even if empty
        state.jobs = response.items || [];
        
        // Update pagination with provided values
        state.pagination = {
          currentPage: response.page,
          pageSize: response.page_size,
          totalItems: response.total,
          totalPages: response.total_pages
        };
        
        state.error = null;
      })
      .addCase(fetchJobs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch jobs';
        state.jobs = [];
      })

      // Fetch Job Details
      .addCase(fetchJobDetails.pending, (state) => {
        state.jobDetailsLoading = true;
        state.jobDetailsError = null;
      })
      .addCase(fetchJobDetails.fulfilled, (state, action) => {
        state.jobDetailsLoading = false;
        state.selectedJob = action.payload;
        state.jobDetailsError = null;
      })
      .addCase(fetchJobDetails.rejected, (state, action) => {
        state.jobDetailsLoading = false;
        state.jobDetailsError = action.payload;
        state.selectedJob = null;
      })

      // Create Job
      .addCase(createJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createJob.fulfilled, (state, action) => {
        state.loading = false;
        state.jobs.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.error = null;
      })
      .addCase(createJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Job
      .addCase(updateJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateJob.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.jobs.findIndex(job => job.id === action.payload.id);
        if (index !== -1) {
          state.jobs[index] = action.payload;
        }
        if (state.selectedJob?.id === action.payload.id) {
          state.selectedJob = action.payload;
        }
        state.error = null;
      })
      .addCase(updateJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Job
      .addCase(deleteJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteJob.fulfilled, (state, action) => {
        state.loading = false;
        state.jobs = state.jobs.filter(job => job.id !== action.payload);
        if (state.selectedJob?.id === action.payload) {
          state.selectedJob = null;
        }
        state.pagination.totalItems -= 1;
        state.error = null;
      })
      .addCase(deleteJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Fetch Related Data
      .addCase(fetchRelatedData.pending, (state) => {
        state.relatedData.loading = true;
        state.relatedData.error = null;
      })
      .addCase(fetchRelatedData.fulfilled, (state, action) => {
        state.relatedData = {
          ...state.relatedData,
          ...action.payload,
          loading: false,
          error: null
        };
      })
      .addCase(fetchRelatedData.rejected, (state, action) => {
        state.relatedData.loading = false;
        state.relatedData.error = action.payload;
      })

      // Update Job Status
      .addCase(updateJobStatus.fulfilled, (state, action) => {
        const index = state.jobs.findIndex(job => job.id === action.payload.id);
        if (index !== -1) {
          state.jobs[index] = action.payload;
        }
        if (state.selectedJob?.id === action.payload.id) {
          state.selectedJob = action.payload;
        }
      });
  }
});

// Action Creators
export const {
  clearJobDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors
} = jobsSlice.actions;

// Selectors
export const selectJobs = state => state.jobs.jobs;
export const selectSelectedJob = state => state.jobs.selectedJob;
export const selectJobDetailsLoading = state => state.jobs.jobDetailsLoading;
export const selectJobDetailsError = state => state.jobs.jobDetailsError;
export const selectLoading = state => state.jobs.loading;
export const selectJobsLoading = state => state.jobs.loading; // Alias for consistency
export const selectError = state => state.jobs.error;
export const selectJobsError = state => state.jobs.error; // Alias for consistency
export const selectFilters = state => state.jobs.filters;
export const selectJobsFilters = state => state.jobs.filters; // Alias for consistency
export const selectPagination = state => state.jobs.pagination;
export const selectJobsPagination = state => state.jobs.pagination; // Alias for consistency
export const selectSorting = state => state.jobs.sorting;
export const selectJobsSorting = state => state.jobs.sorting; // Alias for consistency
export const selectRelatedData = state => state.jobs.relatedData;

// Complex selectors
export const selectFilteredJobs = state => {
  const jobs = selectJobs(state);
  const filters = selectFilters(state);
  
  return jobs.filter(job => {
    const matchesStatus = filters.status === 'ALL' || job.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      job.job_name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      job.job_description?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(job.created_at) >= new Date(filters.dateRange.startDate) &&
       new Date(job.created_at) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesSearch && matchesDateRange;
  });
};

export const selectJobById = (state, jobId) => 
  state.jobs.jobs.find(job => job.id === jobId);

export default jobsSlice.reducer;