// File: /frontend/src/pages/job/JobDetail.jsx
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchJobDetails,
  selectSelectedJob,
  selectJobsLoading,
  selectJobsError
} from '../../store/slices/jobsSlice';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { toast } from 'react-toastify';

const JobDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const job = useSelector(selectSelectedJob);
  const loading = useSelector(selectJobsLoading);
  const error = useSelector(selectJobsError);

  useEffect(() => {
    dispatch(fetchJobDetails(id));
  }, [dispatch, id]);

  if (loading) return <LoadingSpinner />;
  if (error) {
    toast.error(error);
    return (
      <div className="alert alert-danger">
        Error loading job details: {error}
      </div>
    );
  }
  if (!job) return null;

  return (
    <div className="job-detail">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Job Details: {job.job_number}</h2>
        <div className="d-flex gap-2">
          <button
            className="btn btn-outline-primary"
            onClick={() => navigate(`/jobs/${id}/edit`)}
          >
            Edit Job
          </button>
          <button
            className="btn btn-outline-secondary"
            onClick={() => navigate('/jobs')}
          >
            Back to Jobs
          </button>
        </div>
      </div>

      {/* Job Information */}
      <div className="row">
        <div className="col-md-8">
          <div className="card shadow-sm mb-4">
            <div className="card-body">
              <h5 className="card-title mb-4">Job Information</h5>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="text-muted">Job Number</label>
                  <p className="mb-3">{job.job_number}</p>
                </div>
                <div className="col-md-6">
                  <label className="text-muted">Well Name</label>
                  <p className="mb-3">{job.well_name}</p>
                </div>
                <div className="col-md-6">
                  <label className="text-muted">Status</label>
                  <p className="mb-3">
                    <span className={`badge ${
                      job.status === 'Active' ? 'bg-success' :
                      job.status === 'Planned' ? 'bg-primary' :
                      job.status === 'Completed' ? 'bg-info' :
                      'bg-secondary'
                    }`}>
                      {job.status}
                    </span>
                  </p>
                </div>
                <div className="col-md-6">
                  <label className="text-muted">Spud Date</label>
                  <p className="mb-3">
                    {new Date(job.spud_date).toLocaleDateString()}
                  </p>
                </div>
                <div className="col-md-6">
                  <label className="text-muted">Field</label>
                  <p className="mb-3">{job.field}</p>
                </div>
                <div className="col-md-6">
                  <label className="text-muted">Country</label>
                  <p className="mb-3">{job.country}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Additional sections can be added here based on your needs */}
          {/* For example: Well Information, Equipment, Personnel, etc. */}
        </div>

        {/* Sidebar */}
        <div className="col-md-4">
          {/* Quick Actions */}
          <div className="card shadow-sm mb-4">
            <div className="card-body">
              <h5 className="card-title mb-3">Quick Actions</h5>
              <div className="d-grid gap-2">
                <button className="btn btn-outline-primary">
                  View Well Information
                </button>
                <button className="btn btn-outline-primary">
                  View Service Tickets
                </button>
                <button className="btn btn-outline-primary">
                  View Purchase Orders
                </button>
              </div>
            </div>
          </div>

          {/* Job Statistics */}
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="card-title mb-3">Job Statistics</h5>
              {/* Add relevant statistics here */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetail;