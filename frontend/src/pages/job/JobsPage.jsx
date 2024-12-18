// File: /frontend/src/pages/job/JobsPage.jsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchJobs, selectJobs, selectJobsLoading, selectJobsError } from '../../store/slices/jobsSlice';
import JobList from './JobList';
import { Outlet } from 'react-router-dom';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { toast } from 'react-toastify';

const JobsPage = () => {
  const dispatch = useDispatch();
  const jobs = useSelector(selectJobs);
  const loading = useSelector(selectJobsLoading);
  const error = useSelector(selectJobsError);

  useEffect(() => {
    // Fetch jobs when component mounts
    dispatch(fetchJobs());
  }, [dispatch]);

  useEffect(() => {
    // Show error message if there's an error
    if (error) {
      toast.error(error);
    }
  }, [error]);

  if (loading && !jobs.length) {
    return <LoadingSpinner />;
  }

  return (
    <div className="jobs-page">
      <div className="container-fluid">
        <Outlet />
        <JobList />
      </div>
    </div>
  );
};

export default JobsPage;