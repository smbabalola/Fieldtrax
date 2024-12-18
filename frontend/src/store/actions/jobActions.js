// src/store/actions/jobActions.js
import { jobService } from '../../services/jobService';  // Fixed import
import {
  setJobs,
  setJobCenters,
  setOperators,
  setRigs,
  setLoading,
  setError,
  clearError
} from '../slices/jobSlice';

export const fetchJobData = () => async (dispatch) => {
  try {
    dispatch(setLoading(true));
    dispatch(clearError());
    
    const [jobs, centers, operators, rigs] = await Promise.all([
      jobService.getRecentJobs(),
      jobService.getJobCenters(),
      jobService.getOperators(),
      jobService.getRigs()
    ]);

    dispatch(setJobs(jobs));
    dispatch(setJobCenters(centers));
    dispatch(setOperators(operators));
    dispatch(setRigs(rigs));
  } catch (error) {
    dispatch(setError(error.message));
  } finally {
    dispatch(setLoading(false));
  }
};

export const createNewJob = (jobData) => async (dispatch) => {
  try {
    dispatch(setLoading(true));
    dispatch(clearError());
    
    await jobService.createJob(jobData);
    await dispatch(fetchJobData());
  } catch (error) {
    dispatch(setError(error.message));
    throw error;
  } finally {
    dispatch(setLoading(false));
  }
};