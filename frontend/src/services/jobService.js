// jobService.js
import api, { handleApiError } from './api';

// Utility functions
const formatDateForAPI = (date) => {
  if (!date) return null;
  return new Date(date).toISOString();
};

const transformJobDataForAPI = (data) => ({
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
});

const getJobs = async (params) => {
  try {
    // Check network connectivity
    if (!navigator.onLine) {
      throw new Error('No internet connection');
    }

    // Transform frontend pagination params to match backend API
    const apiParams = {
      skip: ((params.page || 1) - 1) * (params.pageSize || 10),
      limit: params.pageSize || 10,
      sort_field: params.sortField || 'created_at',
      sort_order: params.sortOrder || 'desc',
      status: params.status !== 'ALL' ? params.status : undefined,
      search_term: params.searchTerm || undefined
    };

    console.log('Fetching jobs with params:', apiParams);

    const response = await api.get('/jobs', { params: apiParams });

    // Handle empty response
    if (!response) {
      console.warn('Empty response received from jobs endpoint');
      return {
        items: [],
        total: 0,
        page: params.page || 1,
        page_size: params.pageSize || 10,
        total_pages: 0
      };
    }

    // If response is already transformed by interceptor, return it
    if (response.items) {
      return response;
    }

    // Transform array response
    const jobs = Array.isArray(response) ? response : [];
    return {
      items: jobs,
      total: jobs.length,
      page: params.page || 1,
      page_size: params.pageSize || 10,
      total_pages: Math.ceil(jobs.length / (params.pageSize || 10))
    };

  } catch (error) {
    console.error('Error in getJobs:', error);
    throw error;
  }
};

const getAllJobs = () => {
  try {
    return api.get('/jobs');
  } catch (error) {
    return handleApiError(error, 'Failed to fetch all jobs');
  }
};

const getJobById = async (id) => {
  try {
    return await api.get(`/jobs/${id}`);
  } catch (error) {
    return handleApiError(error, `Failed to fetch job with ID: ${id}`);
  }
};

const createJob = async (data) => {
  try {
    const transformedData = transformJobDataForAPI(data);
    return await api.post('/jobs', transformedData);
  } catch (error) {
    return handleApiError(error, 'Failed to create job');
  }
};

const updateJob = async (id, data) => {
  try {
    const transformedData = transformJobDataForAPI(data);
    return await api.put(`/jobs/${id}`, transformedData);
  } catch (error) {
    return handleApiError(error, `Failed to update job with ID: ${id}`);
  }
};

const deleteJob = async (id) => {
  try {
    return await api.delete(`/jobs/${id}`);
  } catch (error) {
    return handleApiError(error, `Failed to delete job with ID: ${id}`);
  }
};

const getActiveJobs = async () => {
  try {
    return await api.get('/jobs/active');
  } catch (error) {
    return handleApiError(error, 'Failed to fetch active jobs');
  }
};

const exportJobs = async () => {
  try {
    return await api.get('/jobs/export');
  } catch (error) {
    return handleApiError(error, 'Failed to export jobs');
  }
};

const getJobsByDateRange = async (startDate, endDate) => {
  try {
    const formattedStartDate = formatDateForAPI(startDate);
    const formattedEndDate = formatDateForAPI(endDate);
    return await api.get(`/jobs/date-range?start=${formattedStartDate}&end=${formattedEndDate}`);
  } catch (error) {
    return handleApiError(error, 'Failed to fetch jobs by date range');
  }
};

const getJobsByStatus = async (status) => {
  try {
    return await api.get(`/jobs/status/${status}`);
  } catch (error) {
    return handleApiError(error, `Failed to fetch jobs with status: ${status}`);
  }
};

const getJobsByCountry = async (country) => {
  try {
    return await api.get(`/jobs/country/${country}`);
  } catch (error) {
    return handleApiError(error, `Failed to fetch jobs for country: ${country}`);
  }
};

const jobService = {
  getJobs,
  getAllJobs,
  getJobById,
  createJob,
  updateJob,
  deleteJob,
  getActiveJobs,
  exportJobs,
  getJobsByDateRange,
  getJobsByStatus,
  getJobsByCountry
};

export default jobService;