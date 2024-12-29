// File: /src/store/index.js
import { configureStore } from '@reduxjs/toolkit';
import wellboreGeometryReducer from './slices/wellboreGeometrySlice';
import trajectoryReducer from './slices/trajectorySlice';
import jobsReducer from './slices/jobsSlice';
import fluidsReducer from './slices/fluidsSlice';
import settingsReducer from './slices/settingsSlice';
import uiReducer from './slices/uiSlice';
import authReducer from './slices/authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    wellboreGeometry: wellboreGeometryReducer,
    trajectory: trajectoryReducer,
    jobs: jobsReducer,
    fluids: fluidsReducer,
    settings: settingsReducer,
    ui: uiReducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false
    })
});

export default store;