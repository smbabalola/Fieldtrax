// File: /frontend/src/store/slices/fluidsSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import fluidService from '../../services/fluidService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchFluids = createAsyncThunk(
  'fluids/fetchFluids',
  async (jobId, { rejectWithValue }) => {
    try {
      // Try to get from cache first
      const cacheKey = `fluids_${jobId}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      // If not in cache, fetch from API
      const response = await fluidService.getFluids(jobId);
      cacheService.set(cacheKey, response);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createFluid = createAsyncThunk(
  'fluids/createFluid',
  async (fluidData, { rejectWithValue }) => {
    try {
      const response = await fluidService.createFluid(fluidData);
      // Invalidate cache after creation
      cacheService.delete(`fluids_${fluidData.jobId}`);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateFluid = createAsyncThunk(
  'fluids/updateFluid',
  async ({ id, ...fluidData }, { rejectWithValue }) => {
    try {
      const response = await fluidService.updateFluid(id, fluidData);
      // Invalidate cache after update
      cacheService.delete(`fluids_${fluidData.jobId}`);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteFluid = createAsyncThunk(
  'fluids/deleteFluid',
  async ({ id, jobId }, { rejectWithValue }) => {
    try {
      await fluidService.deleteFluid(id);
      // Invalidate cache after deletion
      cacheService.delete(`fluids_${jobId}`);
      return id;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchFluidTypes = createAsyncThunk(
  'fluids/fetchFluidTypes',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fluidService.getFluidTypes();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Slice
const fluidsSlice = createSlice({
  name: 'fluids',
  initialState: {
    fluids: [],
    fluidTypes: [],
    selectedFluid: null,
    loading: false,
    error: null,
    createLoading: false,
    updateLoading: false,
    deleteLoading: false,
    lastUpdated: null
  },
  reducers: {
    setSelectedFluid: (state, action) => {
      state.selectedFluid = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    clearSelectedFluid: (state) => {
      state.selectedFluid = null;
    },
    invalidateCache: (state) => {
      state.lastUpdated = new Date().toISOString();
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Fluids
      .addCase(fetchFluids.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFluids.fulfilled, (state, action) => {
        state.loading = false;
        state.fluids = action.payload;
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(fetchFluids.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Create Fluid
      .addCase(createFluid.pending, (state) => {
        state.createLoading = true;
        state.error = null;
      })
      .addCase(createFluid.fulfilled, (state, action) => {
        state.createLoading = false;
        state.fluids.push(action.payload);
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(createFluid.rejected, (state, action) => {
        state.createLoading = false;
        state.error = action.payload;
      })

      // Update Fluid
      .addCase(updateFluid.pending, (state) => {
        state.updateLoading = true;
        state.error = null;
      })
      .addCase(updateFluid.fulfilled, (state, action) => {
        state.updateLoading = false;
        const index = state.fluids.findIndex(fluid => fluid.id === action.payload.id);
        if (index !== -1) {
          state.fluids[index] = action.payload;
        }
        if (state.selectedFluid?.id === action.payload.id) {
          state.selectedFluid = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(updateFluid.rejected, (state, action) => {
        state.updateLoading = false;
        state.error = action.payload;
      })

      // Delete Fluid
      .addCase(deleteFluid.pending, (state) => {
        state.deleteLoading = true;
        state.error = null;
      })
      .addCase(deleteFluid.fulfilled, (state, action) => {
        state.deleteLoading = false;
        state.fluids = state.fluids.filter(fluid => fluid.id !== action.payload);
        if (state.selectedFluid?.id === action.payload) {
          state.selectedFluid = null;
        }
        state.lastUpdated = new Date().toISOString();
      })
      .addCase(deleteFluid.rejected, (state, action) => {
        state.deleteLoading = false;
        state.error = action.payload;
      })

      // Fetch Fluid Types
      .addCase(fetchFluidTypes.fulfilled, (state, action) => {
        state.fluidTypes = action.payload;
      });
  }
});

// Selectors
export const selectAllFluids = (state) => state.fluids.fluids;
export const selectFluidById = (state, fluidId) => 
  state.fluids.fluids.find(fluid => fluid.id === fluidId);
export const selectFluidTypes = (state) => state.fluids.fluidTypes;
export const selectFluidsLoading = (state) => state.fluids.loading;
export const selectFluidsError = (state) => state.fluids.error;
export const selectSelectedFluid = (state) => state.fluids.selectedFluid;

export const {
  setSelectedFluid,
  clearError,
  clearSelectedFluid,
  invalidateCache
} = fluidsSlice.actions;

export default fluidsSlice.reducer;