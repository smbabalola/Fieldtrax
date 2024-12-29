// src/store/slices/wellboreGeometrySlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import wellboreGeometryService from '../../services/wellboreGeometryService';

// Async Thunks
export const fetchWellboreGeometry = createAsyncThunk(
  'wellboreGeometry/fetchWellboreGeometry',
  async (wellboreId) => {
    return await wellboreGeometryService.getWellboreGeometry(wellboreId);
  }
);

export const addCasing = createAsyncThunk(
  'wellboreGeometry/addCasing',
  async ({ wellboreId, casingData }) => {
    return await wellboreGeometryService.addCasing(wellboreId, casingData);
  }
);

export const updateCasing = createAsyncThunk(
  'wellboreGeometry/updateCasing',
  async ({ casingId, casingData }) => {
    return await wellboreGeometryService.updateCasing(casingId, casingData);
  }
);

export const deleteCasing = createAsyncThunk(
  'wellboreGeometry/deleteCasing',
  async (casingId) => {
    await wellboreGeometryService.deleteCasing(casingId);
    return casingId;
  }
);

export const addLiner = createAsyncThunk(
  'wellboreGeometry/addLiner',
  async ({ wellboreId, linerData }) => {
    return await wellboreGeometryService.addLiner(wellboreId, linerData);
  }
);

export const updateLiner = createAsyncThunk(
  'wellboreGeometry/updateLiner',
  async ({ linerId, linerData }) => {
    return await wellboreGeometryService.updateLiner(linerId, linerData);
  }
);

export const deleteLiner = createAsyncThunk(
  'wellboreGeometry/deleteLiner',
  async (linerId) => {
    await wellboreGeometryService.deleteLiner(linerId);
    return linerId;
  }
);

const initialState = {
  casings: [],
  liners: [],
  loading: false,
  error: null,
  selectedCasing: null,
  selectedLiner: null
};

const wellboreGeometrySlice = createSlice({
  name: 'wellboreGeometry',
  initialState,
  reducers: {
    selectCasing: (state, action) => {
      state.selectedCasing = action.payload;
    },
    selectLiner: (state, action) => {
      state.selectedLiner = action.payload;
    },
    clearSelection: (state) => {
      state.selectedCasing = null;
      state.selectedLiner = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Wellbore Geometry
      .addCase(fetchWellboreGeometry.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWellboreGeometry.fulfilled, (state, action) => {
        state.loading = false;
        state.casings = action.payload.casings;
        state.liners = action.payload.liners;
      })
      .addCase(fetchWellboreGeometry.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      
      // Add Casing
      .addCase(addCasing.fulfilled, (state, action) => {
        state.casings.push(action.payload);
      })
      
      // Update Casing
      .addCase(updateCasing.fulfilled, (state, action) => {
        const index = state.casings.findIndex(c => c.id === action.payload.id);
        if (index !== -1) {
          state.casings[index] = action.payload;
        }
      })
      
      // Delete Casing
      .addCase(deleteCasing.fulfilled, (state, action) => {
        state.casings = state.casings.filter(c => c.id !== action.payload);
      })
      
      // Add Liner
      .addCase(addLiner.fulfilled, (state, action) => {
        state.liners.push(action.payload);
      })
      
      // Update Liner
      .addCase(updateLiner.fulfilled, (state, action) => {
        const index = state.liners.findIndex(l => l.id === action.payload.id);
        if (index !== -1) {
          state.liners[index] = action.payload;
        }
      })
      
      // Delete Liner
      .addCase(deleteLiner.fulfilled, (state, action) => {
        state.liners = state.liners.filter(l => l.id !== action.payload);
      });
  }
});

// Selectors
export const selectCasings = (state) => state.wellboreGeometry.casings;
export const selectLiners = (state) => state.wellboreGeometry.liners;
export const selectLoading = (state) => state.wellboreGeometry.loading;
export const selectError = (state) => state.wellboreGeometry.error;
export const selectSelectedCasing = (state) => state.wellboreGeometry.selectedCasing;
export const selectSelectedLiner = (state) => state.wellboreGeometry.selectedLiner;

export const { selectCasing, selectLiner, clearSelection } = wellboreGeometrySlice.actions;

export default wellboreGeometrySlice.reducer;