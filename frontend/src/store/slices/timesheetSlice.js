// src/store/slices/timesheetSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import timesheetService from '../../services/timesheetService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchTimesheets = createAsyncThunk(
  'timesheets/fetchTimesheets',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `timesheets_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await timesheetService.getTimeSheets(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchTimesheetsByJob = createAsyncThunk(
  'timesheets/fetchTimesheetsByJob',
  async (jobId, { rejectWithValue }) => {
    try {
      const response = await timesheetService.getTimesheetsByJob(jobId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchTimesheetsByEmployee = createAsyncThunk(
  'timesheets/fetchTimesheetsByEmployee',
  async (employeeId, { rejectWithValue }) => {
    try {
      const response = await timesheetService.getTimesheetsByEmployee(employeeId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createTimesheet = createAsyncThunk(
  'timesheets/createTimesheet',
  async (timesheetData, { rejectWithValue }) => {
    try {
      const validation = timesheetService.validateTimesheetData(timesheetData);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await timesheetService.createTimeSheet(timesheetData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateTimesheet = createAsyncThunk(
  'timesheets/updateTimesheet',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const validation = timesheetService.validateTimesheetData(data);
      if (!validation.isValid) {
        return rejectWithValue(validation.errors);
      }
      const response = await timesheetService.updateTimeSheet(id, data);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteTimesheet = createAsyncThunk(
  'timesheets/deleteTimesheet',
  async (timesheetId, { rejectWithValue }) => {
    try {
      await timesheetService.deleteTimeSheet(timesheetId);
      cacheService.clear();
      return timesheetId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const approveTimesheet = createAsyncThunk(
  'timesheets/approveTimesheet',
  async ({ timesheetId, approverNotes }, { rejectWithValue }) => {
    try {
      const response = await timesheetService.approveTimeSheet(timesheetId, approverNotes);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchPendingTimesheets = createAsyncThunk(
  'timesheets/fetchPendingTimesheets',
  async (_, { rejectWithValue }) => {
    try {
      const response = await timesheetService.getPendingTimesheets();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const calculateTotalHours = createAsyncThunk(
  'timesheets/calculateTotalHours',
  async (params, { rejectWithValue }) => {
    try {
      const response = await timesheetService.calculateTotalHours(params);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  employeeId: null,
  jobId: null,
  dateRange: {
    startDate: null,
    endDate: null
  }
};

// Initial State
const initialState = {
  timesheets: [],
  pendingTimesheets: [],
  selectedTimesheet: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  timesheetDetailsLoading: false,
  error: null,
  timesheetDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'date',
    order: 'desc'
  },
  statistics: {
    totalHours: 0,
    averageHoursPerDay: 0,
    totalOvertime: 0,
    pendingCount: 0
  },
  lastUpdated: null
};

// Slice
const timesheetSlice = createSlice({
  name: 'timesheets',
  initialState,
  reducers: {
    clearTimesheetDetails: (state) => {
      state.selectedTimesheet = null;
      state.timesheetDetailsError = null;
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
      state.timesheetDetailsError = null;
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
      // Fetch Timesheets
      .addCase(fetchTimesheets.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTimesheets.fulfilled, (state, action) => {
        state.loading = false;
        state.timesheets = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchTimesheets.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch timesheets';
        state.timesheets = [];
      })

      // Fetch Pending Timesheets
      .addCase(fetchPendingTimesheets.fulfilled, (state, action) => {
        state.pendingTimesheets = action.payload || [];
        state.statistics.pendingCount = action.payload?.length || 0;
      })

      // Create Timesheet
      .addCase(createTimesheet.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createTimesheet.fulfilled, (state, action) => {
        state.loading = false;
        state.timesheets.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createTimesheet.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Timesheet
      .addCase(updateTimesheet.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateTimesheet.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.timesheets.findIndex(ts => ts.id === action.payload.id);
        if (index !== -1) {
          state.timesheets[index] = action.payload;
        }
        if (state.selectedTimesheet?.id === action.payload.id) {
          state.selectedTimesheet = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateTimesheet.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Timesheet
      .addCase(deleteTimesheet.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteTimesheet.fulfilled, (state, action) => {
        state.loading = false;
        state.timesheets = state.timesheets.filter(ts => ts.id !== action.payload);
        if (state.selectedTimesheet?.id === action.payload) {
          state.selectedTimesheet = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteTimesheet.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Approve Timesheet
      .addCase(approveTimesheet.fulfilled, (state, action) => {
        const index = state.timesheets.findIndex(ts => ts.id === action.payload.id);
        if (index !== -1) {
          state.timesheets[index] = action.payload;
        }
        if (state.selectedTimesheet?.id === action.payload.id) {
          state.selectedTimesheet = action.payload;
        }
        state.pendingTimesheets = state.pendingTimesheets.filter(
          ts => ts.id !== action.payload.id
        );
        state.statistics.pendingCount = state.pendingTimesheets.length;
        state.lastUpdated = new Date().toISOString();
      })

      // Calculate Total Hours
      .addCase(calculateTotalHours.fulfilled, (state, action) => {
        state.statistics = {
          ...state.statistics,
          ...action.payload
        };
      });
  }
});

// Action Creators
export const {
  clearTimesheetDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateStatistics
} = timesheetSlice.actions;

// Basic Selectors
export const selectTimesheets = state => state.timesheets.timesheets;
export const selectPendingTimesheets = state => state.timesheets.pendingTimesheets;
export const selectSelectedTimesheet = state => state.timesheets.selectedTimesheet;
export const selectLoading = state => state.timesheets.loading;
export const selectError = state => state.timesheets.error;
export const selectPagination = state => state.timesheets.pagination;
export const selectFilters = state => state.timesheets.filters;
export const selectSorting = state => state.timesheets.sorting;
export const selectStatistics = state => state.timesheets.statistics;
export const selectLastUpdated = state => state.timesheets.lastUpdated;

// Complex Selectors
export const selectFilteredTimesheets = state => {
  const timesheets = selectTimesheets(state);
  const filters = selectFilters(state);
  
  return timesheets.filter(timesheet => {
    const matchesStatus = filters.status === 'ALL' || timesheet.status === filters.status;
    const matchesEmployee = !filters.employeeId || timesheet.employee_id === filters.employeeId;
    const matchesJob = !filters.jobId || timesheet.job_id === filters.jobId;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(timesheet.date) >= new Date(filters.dateRange.startDate) &&
       new Date(timesheet.date) <= new Date(filters.dateRange.endDate));

    return matchesStatus && matchesEmployee && matchesJob && matchesDateRange;
  });
};

export const selectTimesheetById = (state, timesheetId) => 
  state.timesheets.timesheets.find(timesheet => timesheet.id === timesheetId);

export default timesheetSlice.reducer;