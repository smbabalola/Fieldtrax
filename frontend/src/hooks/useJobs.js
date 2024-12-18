import { useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchJobs,
  createJob,
  fetchJobDetails,
  searchJobs,
  setFilter,
  clearFilters,
  selectJobs,
  selectSelectedJob,
  selectJobsLoading,
  selectJobsError,
  selectJobFilters,
  selectSearchResults,
  selectSearchLoading
} from '../store/slices/jobsSlice';

export const useJobs = () => {
  const dispatch = useDispatch();
  
  // Selectors
  const jobs = useSelector(selectJobs);
  const selectedJob = useSelector(selectSelectedJob);
  const loading = useSelector(selectJobsLoading);
  const error = useSelector(selectJobsError);
  const filters = useSelector(selectJobFilters);
  const searchResults = useSelector(selectSearchResults);
  const searchLoading = useSelector(selectSearchLoading);

  // Actions
  const loadJobs = useCallback((params) => {
    dispatch(fetchJobs(params));
  }, [dispatch]);

  const loadJobDetails = useCallback((jobId) => {
    dispatch(fetchJobDetails(jobId));
  }, [dispatch]);

  const handleCreateJob = useCallback(async (jobData) => {
    try {
      const result = await dispatch(createJob(jobData)).unwrap();
      return { success: true, data: result };
    } catch (error) {
      return { success: false, error };
    }
  }, [dispatch]);

  const handleSearch = useCallback((query) => {
    dispatch(setFilter({ searchQuery: query }));
    if (query.length >= 2) {
      dispatch(searchJobs(query));
    }
  }, [dispatch]);

  const handleFilter = useCallback((filterParams) => {
    dispatch(setFilter(filterParams));
    dispatch(fetchJobs({ ...filters, ...filterParams }));
  }, [dispatch, filters]);

  const resetFilters = useCallback(() => {
    dispatch(clearFilters());
    dispatch(fetchJobs());
  }, [dispatch]);

  // Load jobs on mount
  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  return {
    // State
    jobs,
    selectedJob,
    loading,
    error,
    filters,
    searchResults,
    searchLoading,

    // Actions
    loadJobs,
    loadJobDetails,
    createJob: handleCreateJob,
    searchJobs: handleSearch,
    setFilter: handleFilter,
    resetFilters
  };
};

export default useJobs;