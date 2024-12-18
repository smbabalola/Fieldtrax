// src/services/jobService.js
import axios from '../utils/axios';

const JOB_API_URL = '/jobs';

// Create axios instance with custom config
const axiosInstance = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Format dates for API
const formatDateForAPI = (date) => {
  if (!date) return null;
  return new Date(date).toISOString();
};

// Transform job data for API
const transformJobDataForAPI = (data) => {
  return {
    jobcenter_id: data.jobcenter_id || null,
    job_name: data.job_name,
    job_description: data.job_description || null,
    rig_id: data.rig_id || null,
    purchase_order_id: data.purchase_order_id || null,
    operator_id: data.operator_id || null,
    well_id: data.well_id || null,
    service_code: data.service_code || null,
    country: data.country || null,
    measured_depth: data.measured_depth ? Number(data.measured_depth) : null,
    total_vertical_depth: data.total_vertical_depth ? Number(data.total_vertical_depth) : null,
    spud_date: formatDateForAPI(data.spud_date),
    status: data.status || 'Planned',
    mobilization_date: formatDateForAPI(data.mobilization_date),
    demobilization_date: formatDateForAPI(data.demobilization_date),
    job_closed: Boolean(data.job_closed),
    trainingfile: Boolean(data.trainingfile)
  };
};
const handleError = (error, customMessage) => {
  console.error('API Error:', error);
  console.error('Error Response Data:', error.response?.data);
  console.error('Error Config Data:', error.config?.data);
  
  if (axios.isCancel(error)) {
    throw new Error('Request was cancelled');
  }

  if (error.code === 'ECONNABORTED') {
    throw new Error('Request timed out - please try again');
  }

  if (error.response) {
    let errorMessage;
    if (error.response.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response.data?.message) {
      errorMessage = error.response.data.message;
    } else if (typeof error.response.data === 'string') {
      errorMessage = error.response.data;
    } else if (error.response.status === 400) {
      errorMessage = 'Invalid data submitted. Please check all required fields.';
    } else {
      errorMessage = `Server error: ${error.response.status}`;
    }
    throw new Error(errorMessage);
  }

  if (error.request) {
    throw new Error('No response from server - please check your connection');
  }

  throw new Error(error.message || customMessage || 'An unexpected error occurred');
};

const jobService = {
  // Create job with proper validation and transformation
  createJob: async (jobData) => {
    try {
      // Transform and validate the data
      const transformedData = transformJobDataForAPI(jobData);
      
      // Send request
      const response = await axiosInstance.post(JOB_API_URL, transformedData);
      
      return response.data;
    } catch (error) {
      handleError(error, 'Failed to create job');
    }
  },

  getJobs: async (params = {}) => {
    try {
      const { page = 1, pageSize = 10, ...otherParams } = params;
      
      const queryParams = {
        skip: (page - 1) * pageSize,
        limit: pageSize,
        ...otherParams
      };

      const response = await axiosInstance.get(JOB_API_URL, { params: queryParams });
      
      const items = Array.isArray(response.data) ? response.data : 
                    Array.isArray(response.data.items) ? response.data.items : [];
      
      return {
        items,
        page,
        page_size: pageSize,
        total: response.data.total || items.length,
        total_pages: response.data.total_pages || Math.ceil(items.length / pageSize)
      };
    } catch (error) {
      handleError(error, 'Failed to fetch jobs');
    }
  },

  getJob: async (jobId) => {
    try {
      const response = await axiosInstance.get(`${JOB_API_URL}/${jobId}`);
      return response.data;
    } catch (error) {
      handleError(error, `Failed to fetch job ${jobId}`);
    }
  },

  updateJob: async (jobId, jobData) => {
    try {
      const transformedData = transformJobDataForAPI(jobData);
      const response = await axiosInstance.put(`${JOB_API_URL}/${jobId}`, transformedData);
      return response.data;
    } catch (error) {
      handleError(error, `Failed to update job ${jobId}`);
    }
  }
};

export default jobService;