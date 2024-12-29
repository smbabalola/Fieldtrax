// File: /src/services/timesheetService.js
import api, { API_ENDPOINTS, handleApiError } from './api';

// Utility function to format dates for API
const formatDateForAPI = (date) => {
  if (!date) return null;
  try {
    return new Date(date).toISOString();
  } catch (e) {
    console.error('Date formatting error:', e);
    return null;
  }
};

// Transform timesheet data for API
const transformTimesheetData = (data) => ({
  job_id: data.job_id,
  employee_id: data.employee_id,
  date: formatDateForAPI(data.date),
  start_time: data.start_time,
  end_time: data.end_time,
  hours_worked: Number(data.hours_worked),
  break_time: Number(data.break_time) || 0,
  overtime_hours: Number(data.overtime_hours) || 0,
  activity_type: data.activity_type,
  description: data.description || '',
  location: data.location || '',
  status: data.status || 'pending',
  notes: data.notes || '',
  created_at: formatDateForAPI(new Date()),
  updated_at: formatDateForAPI(new Date())
});

const timesheetService = {
  // Core Timesheet Operations
  getTimeSheets: async (params = {}) => {
    try {
      const queryParams = {
        skip: params.page ? (params.page - 1) * (params.limit || 10) : 0,
        limit: params.limit || 10,
        job_id: params.job_id,
        employee_id: params.employee_id,
        status: params.status,
        start_date: formatDateForAPI(params.start_date),
        end_date: formatDateForAPI(params.end_date),
        sort_by: params.sort_by || 'date',
        sort_direction: params.sort_direction || 'desc',
        ...params.filters
      };

      const response = await api.get(API_ENDPOINTS.timeSheets.base, { params: queryParams });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets');
    }
  },

  getTimesheetById: async (timesheetId) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.timeSheets.base}/${timesheetId}`);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheet details');
    }
  },

  createTimeSheet: async (timesheetData) => {
    try {
      // Validate data before sending
      const validation = timesheetService.validateTimesheetData(timesheetData);
      if (!validation.isValid) {
        throw new Error(`Validation failed: ${JSON.stringify(validation.errors)}`);
      }

      const transformedData = transformTimesheetData(timesheetData);
      const response = await api.post(API_ENDPOINTS.timeSheets.base, transformedData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error creating timesheet');
    }
  },

  updateTimeSheet: async (timesheetId, timesheetData) => {
    try {
      const transformedData = transformTimesheetData(timesheetData);
      const response = await api.put(
        `${API_ENDPOINTS.timeSheets.base}/${timesheetId}`, 
        transformedData
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating timesheet');
    }
  },

  deleteTimeSheet: async (timesheetId) => {
    try {
      await api.delete(`${API_ENDPOINTS.timeSheets.base}/${timesheetId}`);
      return true;
    } catch (error) {
      return handleApiError(error, 'Error deleting timesheet');
    }
  },

  // Job-specific Operations
  getTimesheetsByJob: async (jobId, params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.timeSheets.getByJob(jobId), { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets for job');
    }
  },

  // Employee-specific Operations
  getTimesheetsByEmployee: async (employeeId, params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.timeSheets.getByEmployee(employeeId), { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets for employee');
    }
  },

  // Date Range Operations
  getTimesheetsByDateRange: async (startDate, endDate, params = {}) => {
    try {
      const queryParams = {
        ...params,
        start_date: formatDateForAPI(startDate),
        end_date: formatDateForAPI(endDate)
      };

      const response = await api.get(API_ENDPOINTS.timeSheets.getByDateRange, { params: queryParams });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets for date range');
    }
  },

  // Approval Operations
  getPendingTimeSheets: async (params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.timeSheets.getPending, { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching pending timesheets');
    }
  },

  approveTimeSheet: async (timesheetId, approverNotes = '') => {
    try {
      const response = await api.post(
        `${API_ENDPOINTS.timeSheets.base}/${timesheetId}/approve`,
        { notes: approverNotes }
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error approving timesheet');
    }
  },

  rejectTimeSheet: async (timesheetId, rejectionReason) => {
    try {
      const response = await api.post(
        `${API_ENDPOINTS.timeSheets.base}/${timesheetId}/reject`,
        { reason: rejectionReason }
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error rejecting timesheet');
    }
  },

  // Hour Calculations
  calculateTotalHours: async (params = {}) => {
    try {
      const response = await api.get(API_ENDPOINTS.timeSheets.getTotalHours, { params });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error calculating total hours');
    }
  },

  // Batch Operations
  batchApproveTimeSheets: async (timesheetIds, approverNotes = '') => {
    try {
      const response = await api.post(`${API_ENDPOINTS.timeSheets.base}/batch-approve`, {
        timesheet_ids: timesheetIds,
        notes: approverNotes
      });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error batch approving timesheets');
    }
  },

  batchUpdateTimeSheets: async (updates) => {
    try {
      const response = await api.put(`${API_ENDPOINTS.timeSheets.base}/batch`, { updates });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error performing batch update');
    }
  },

  // Report Generation
  generateTimesheetReport: async (params = {}) => {
    try {
      const response = await api.get(
        `${API_ENDPOINTS.timeSheets.base}/report`,
        { params, responseType: 'blob' }
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error generating timesheet report');
    }
  },

  // Statistics
  getTimesheetStatistics: async (params = {}) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.timeSheets.base}/statistics`, { params });
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheet statistics');
    }
  },

  // Validation
  validateTimesheetData: (data) => {
    const errors = {};

    // Required fields
    if (!data.job_id) {
      errors.job_id = 'Job ID is required';
    }

    if (!data.employee_id) {
      errors.employee_id = 'Employee ID is required';
    }

    if (!data.date) {
      errors.date = 'Date is required';
    }

    // Time validations
    if (!data.start_time) {
      errors.start_time = 'Start time is required';
    }

    if (!data.end_time) {
      errors.end_time = 'End time is required';
    }

    // Numeric validations
    if (isNaN(Number(data.hours_worked)) || Number(data.hours_worked) <= 0) {
      errors.hours_worked = 'Valid hours worked are required';
    }

    if (data.break_time && isNaN(Number(data.break_time))) {
      errors.break_time = 'Break time must be a number';
    }

    if (data.overtime_hours && isNaN(Number(data.overtime_hours))) {
      errors.overtime_hours = 'Overtime hours must be a number';
    }

    // Business logic validations
    if (data.start_time && data.end_time) {
      const start = new Date(`1970-01-01T${data.start_time}`);
      const end = new Date(`1970-01-01T${data.end_time}`);
      if (start >= end) {
        errors.time = 'End time must be after start time';
      }
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  },

  /**
   * Get timesheets by status
   * @param {string} status Timesheet status
   * @param {Object} params Additional query parameters
   * @returns {Promise<Array>} List of timesheets
   */
  getTimesheetsByStatus: async (status, params = {}) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.timeSheets.base}/status/${status}`, { params });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets by status');
    }
  },

  /**
   * Get timesheets by date range and employee ID
   * @param {string} startDate Start date
   * @param {string} endDate End date
   * @param {string} employeeId Employee ID
   * @param {Object} params Additional query parameters
   * @returns {Promise<Array>} List of timesheets
   */
  getTimesheetsByDateAndEmployee: async (startDate, endDate, employeeId, params = {}) => {
    try {
      const queryParams = {
        ...params,
        start_date: formatDateForAPI(startDate),
        end_date: formatDateForAPI(endDate),
        employee_id: employeeId
      };

      const response = await api.get(API_ENDPOINTS.timeSheets.getByDateRange, { params: queryParams });
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching timesheets by date and employee');
    }
  },

  createTimesheet: async (timesheetData) => {
    try {
      const response = await api.post('/timesheet', timesheetData);
      return response.data;
    } catch (error) {
      console.error('Error creating timesheet:', error);
      throw error;
    }
  },

  getTimesheetsByJob: async (jobId) => {
    try {
      const response = await api.get(`/timesheet/job/${jobId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching timesheets by job:', error);
      throw error;
    }
  },

  getTimesheetsByEmployee: async (employeeId) => {
    try {
      const response = await api.get(`/timesheet/employee/${employeeId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching timesheets by employee:', error);
      throw error;
    }
  },

  getPendingTimesheets: async () => {
    try {
      const response = await api.get('/timesheet/pending');
      return response.data;
    } catch (error) {
      console.error('Error fetching pending timesheets:', error);
      throw error;
    }
  },

  approveTimesheet: async (timesheetId) => {
    try {
      const response = await api.post(`/timesheet/${timesheetId}/approve`);
      return response.data;
    } catch (error) {
      console.error('Error approving timesheet:', error);
      throw error;
    }
  },

  getTimesheetsByDateRange: async (startDate, endDate, employeeId) => {
    try {
      const response = await api.get('/timesheet/date-range', {
        params: { startDate, endDate, employeeId }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching timesheets by date range:', error);
      throw error;
    }
  },

  calculateTotalHours: async (employeeId, startDate, endDate) => {
    try {
      const response = await api.get('/timesheet/hours/total', {
        params: { employeeId, startDate, endDate }
      });
      return response.data;
    } catch (error) {
      console.error('Error calculating total hours:', error);
      throw error;
    }
  },

  updateTimesheet: async (timesheetId, timesheetData) => {
    try {
      const response = await api.put(`/timesheet/${timesheetId}`, timesheetData);
      return response.data;
    } catch (error) {
      console.error('Error updating timesheet:', error);
      throw error;
    }
  }
};

export default timesheetService;