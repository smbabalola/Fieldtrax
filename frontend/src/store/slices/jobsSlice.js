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
      const response = await jobService.getJob(jobId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createJob = createAsyncThunk(
  'jobs/createJob',
  async (jobData, { rejectWithValue }) => {
    try {
      const response = await jobService.createJob(jobData);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateJob = createAsyncThunk(
  'jobs/updateJob',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await jobService.updateJob(id, data);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteJob = createAsyncThunk(
  'jobs/deleteJob',
  async (jobId, { rejectWithValue }) => {
    try {
      await jobService.deleteJob(jobId);
      return jobId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateJobStatus = createAsyncThunk(
  'jobs/updateJobStatus',
  async ({ jobId, status }, { rejectWithValue }) => {
    try {
      const response = await jobService.updateJobStatus(jobId, status);
      return response;
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
        jobService.fetchRigs(),
        jobService.fetchWells(),
        jobService.fetchOperators(),
        jobService.fetchPurchaseOrders()
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

const initialFilters = {
  status: 'ALL',
  priority: 'ALL',
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
  relatedData: {
    rigs: [],
    wells: [],
    operators: [],
    purchaseOrders: [],
    loading: false,
    error: null
  },
  filters: {
    status: 'ALL',
    priority: 'ALL',
    searchTerm: '',
    dateRange: {
      startDate: null,
      endDate: null
    }
  },
  sorting: {
    field: 'created_at',
    direction: 'desc'
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
    },
    resetFilters: (state) => {
      state.filters = initialFilters;
    },
    setSorting: (state, action) => {
      state.sorting = action.payload;
    },
    setPagination: (state, action) => {
      state.pagination = {
        ...state.pagination,
        ...action.payload
      };
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
      state.jobDetailsError = null;
      state.relatedData.error = null;
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
        state.jobs = action.payload.items;
        state.pagination = {
          currentPage: action.payload.page,
          pageSize: action.payload.page_size,
          totalItems: action.payload.total,
          totalPages: action.payload.total_pages
        };
      })
      .addCase(fetchJobs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Fetch Job Details
      .addCase(fetchJobDetails.pending, (state) => {
        state.jobDetailsLoading = true;
        state.jobDetailsError = null;
      })
      .addCase(fetchJobDetails.fulfilled, (state, action) => {
        state.jobDetailsLoading = false;
        state.selectedJob = action.payload;
      })
      .addCase(fetchJobDetails.rejected, (state, action) => {
        state.jobDetailsLoading = false;
        state.jobDetailsError = action.payload;
      })

      // Create Job
      .addCase(createJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createJob.fulfilled, (state, action) => {
        state.loading = false;
        state.jobs.unshift(action.payload);
        // Update total items count
        state.pagination.totalItems += 1;
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
        // Update selected job if it's the one being updated
        if (state.selectedJob?.id === action.payload.id) {
          state.selectedJob = action.payload;
        }
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
        // Update total items count
        state.pagination.totalItems -= 1;
      })
      .addCase(deleteJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
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
      });
  }
});

// Action Creators
export const {
  clearJobDetails,
  setFilter,
  setFilters,
  resetFilters,
  setSorting,
  setPagination,
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
export const selectJobsLoading = state => state.jobs.loading; 
export const selectError = state => state.jobs.error;
export const selectJobsError = state => state.jobs.error;
export const selectFilters = state => state.jobs.filters;
export const selectPagination = state => state.jobs.pagination;
export const selectJobsPagination = state => state.jobs.pagination; 
export const selectJobsFilters = state => state.jobs.filters;
export const selectSorting = state => state.jobs.sorting;
export const selectJobsSorting = state => state.jobs.sorting; 
export const selectRelatedData = state => state.jobs.relatedData;

// Complex selectors
export const selectFilteredJobs = state => {
  const jobs = selectJobs(state);
  const filters = selectJobsFilters(state);
  
  return jobs.filter(job => {
    const matchesStatus = filters.status === 'ALL' || job.status === filters.status;
    const matchesPriority = filters.priority === 'ALL' || job.priority === filters.priority;
    const matchesSearch = !filters.searchTerm || 
      job.description?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      job.job_number?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      job.notes?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(job.start_date) >= new Date(filters.dateRange.startDate) &&
       new Date(job.start_date) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesPriority && matchesSearch && matchesDateRange;
  });
};

export const selectJobById = (state, jobId) => 
  state.jobs.jobs.find(job => job.id === jobId);

export default jobsSlice.reducer;