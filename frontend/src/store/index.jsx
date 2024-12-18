import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import settingsReducer from './slices/settingsSlice';
import jobsReducer from './slices/jobsSlice';
import uiReducer from './slices/uiSlice';
import fluidsReducer from './slices/fluidsSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    settings: settingsReducer,
    jobs: jobsReducer,
    ui: uiReducer,
    fluids: fluidsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['jobs/createJob/fulfilled', 'jobs/fetchJobs/fulfilled'],
        // Ignore these field paths in all actions
        ignoredActionPaths: ['payload.timestamp', 'payload.dates'],
        // Ignore these paths in the state
        ignoredPaths: ['jobs.selectedJob.dates'],
      },
    }),
});

export default store;