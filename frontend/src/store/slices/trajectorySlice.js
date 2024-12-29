// src/store/slices/trajectorySlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import trajectoryService from '../../services/trajectoryService';

export const fetchTrajectoryData = createAsyncThunk(
  'trajectory/fetchTrajectoryData',
  async (wellId) => {
    return await trajectoryService.getTrajectoryData(wellId);
  }
);

export const addTrajectoryPoint = createAsyncThunk(
  'trajectory/addTrajectoryPoint',
  async ({ wellId, pointData }) => {
    return await trajectoryService.addTrajectoryPoint(wellId, pointData);
  }
);

export const updateTrajectoryPoint = createAsyncThunk(
  'trajectory/updateTrajectoryPoint',
  async ({ pointId, pointData }) => {
    return await trajectoryService.updateTrajectoryPoint(pointId, pointData);
  }
);

const initialState = {
  trajectoryPoints: [],
  loading: false,
  error: null,
  selectedPoint: null,
  totalDepth: 0,
  maxInclination: 0
};

const trajectorySlice = createSlice({
  name: 'trajectory',
  initialState,
  reducers: {
    selectPoint: (state, action) => {
      state.selectedPoint = action.payload;
    },
    clearSelection: (state) => {
      state.selectedPoint = null;
    },
    updateTotalDepth: (state, action) => {
      state.totalDepth = action.payload;
    },
    updateMaxInclination: (state, action) => {
      state.maxInclination = Math.max(...state.trajectoryPoints.map(p => p.inclination));
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTrajectoryData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTrajectoryData.fulfilled, (state, action) => {
        state.loading = false;
        state.trajectoryPoints = action.payload;
        state.maxInclination = Math.max(...action.payload.map(p => p.inclination));
      })
      .addCase(fetchTrajectoryData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(addTrajectoryPoint.fulfilled, (state, action) => {
        state.trajectoryPoints.push(action.payload);
        state.maxInclination = Math.max(...state.trajectoryPoints.map(p => p.inclination));
      })
      .addCase(updateTrajectoryPoint.fulfilled, (state, action) => {
        const index = state.trajectoryPoints.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.trajectoryPoints[index] = action.payload;
          state.maxInclination = Math.max(...state.trajectoryPoints.map(p => p.inclination));
        }
      });
  }
});

export const { selectPoint, clearSelection, updateTotalDepth, updateMaxInclination } = trajectorySlice.actions;

export default trajectorySlice.reducer;