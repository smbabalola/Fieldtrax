// src/store/slices/uiSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  jobDetailsModal: {
    isOpen: false,
    selectedJob: null,
    loading: false,
    error: null
  },
  createJobModal: {
    isOpen: false,
    loading: false,
    error: null
  },
  columnSettings: {
    isOpen: false,
    columns: {
      job_name: { 
        title: 'Job Name', 
        visible: true, 
        order: 1,
        width: '20%'
      },
      status: { 
        title: 'Status', 
        visible: true, 
        order: 2,
        width: '10%'
      },
      well: { 
        title: 'Well Info', 
        visible: true, 
        order: 3,
        width: '20%'
      },
      operator: { 
        title: 'Operator', 
        visible: true, 
        order: 4,
        width: '20%'
      },
      rig: { 
        title: 'Rig', 
        visible: true, 
        order: 5,
        width: '15%'
      },
      dates: { 
        title: 'Dates', 
        visible: true, 
        order: 6,
        width: '15%'
      }
    }
  }
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // Job Details Modal actions
    openJobDetailsModal: (state, action) => {
      state.jobDetailsModal.isOpen = true;
      state.jobDetailsModal.selectedJob = action.payload;
      state.jobDetailsModal.loading = false;
      state.jobDetailsModal.error = null;
    },
    closeJobDetailsModal: (state) => {
      state.jobDetailsModal.isOpen = false;
      state.jobDetailsModal.selectedJob = null;
      state.jobDetailsModal.loading = false;
      state.jobDetailsModal.error = null;
    },
    setJobDetailsLoading: (state, action) => {
      state.jobDetailsModal.loading = action.payload;
    },
    setJobDetailsError: (state, action) => {
      state.jobDetailsModal.error = action.payload;
      state.jobDetailsModal.loading = false;
    },

    // Create Job Modal actions
    openCreateJobModal: (state) => {
      state.createJobModal.isOpen = true;
      state.createJobModal.loading = false;
      state.createJobModal.error = null;
    },
    closeCreateJobModal: (state) => {
      state.createJobModal.isOpen = false;
      state.createJobModal.loading = false;
      state.createJobModal.error = null;
    },
    setCreateJobLoading: (state, action) => {
      state.createJobModal.loading = action.payload;
    },
    setCreateJobError: (state, action) => {
      state.createJobModal.error = action.payload;
      state.createJobModal.loading = false;
    },

    // Column Settings actions
    toggleColumnSettings: (state) => {
      state.columnSettings.isOpen = !state.columnSettings.isOpen;
    },
    updateColumnVisibility: (state, action) => {
      const { columnId, visible } = action.payload;
      if (state.columnSettings.columns[columnId]) {
        state.columnSettings.columns[columnId].visible = visible;
      }
    },
    updateColumnOrder: (state, action) => {
      const { columnId, order } = action.payload;
      if (state.columnSettings.columns[columnId]) {
        state.columnSettings.columns[columnId].order = order;
      }
    },
    resetColumnSettings: (state) => {
      state.columnSettings = initialState.columnSettings;
    }
  }
});

// Export actions
export const {
  openJobDetailsModal,
  closeJobDetailsModal,
  setJobDetailsLoading,
  setJobDetailsError,
  openCreateJobModal,
  closeCreateJobModal,
  setCreateJobLoading,
  setCreateJobError,
  toggleColumnSettings,
  updateColumnVisibility,
  updateColumnOrder,
  resetColumnSettings
} = uiSlice.actions;

// Export selectors
export const selectJobDetailsModal = (state) => state.ui.jobDetailsModal;
export const selectCreateJobModal = (state) => state.ui.createJobModal;
export const selectColumnSettings = (state) => state.ui.columnSettings;
export const selectTableColumns = (state) => state.ui.columnSettings.columns;

export default uiSlice.reducer;
