// File: /frontend/src/pages/job/JobForm.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { createJob, fetchJobDetails, selectSelectedJob, selectJobsLoading } from '../../store/slices/jobsSlice';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { toast } from 'react-toastify';

const JobForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const isEdit = !!id;

  const selectedJob = useSelector(selectSelectedJob);
  const loading = useSelector(selectJobsLoading);

  const [formData, setFormData] = useState({
    job_number: '',
    well_name: '',
    status: 'PLANNED',
    spud_date: '',
    field: '',
    country: '',
    rig_name: '',
    operator: '',
    total_depth: '',
    well_type: '',
    description: '',
  });

  useEffect(() => {
    if (isEdit && id) {
      dispatch(fetchJobDetails(id));
    }
  }, [dispatch, id, isEdit]);

  useEffect(() => {
    if (isEdit && selectedJob) {
      setFormData({
        job_number: selectedJob.job_number || '',
        well_name: selectedJob.well_name || '',
        status: selectedJob.status || 'PLANNED',
        spud_date: selectedJob.spud_date ? new Date(selectedJob.spud_date).toISOString().split('T')[0] : '',
        field: selectedJob.field || '',
        country: selectedJob.country || '',
        rig_name: selectedJob.rig_name || '',
        operator: selectedJob.operator || '',
        total_depth: selectedJob.total_depth || '',
        well_type: selectedJob.well_type || '',
        description: selectedJob.description || '',
      });
    }
  }, [selectedJob, isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(createJob(formData)).unwrap();
      toast.success(`Job ${isEdit ? 'updated' : 'created'} successfully`);
      navigate('/jobs');
    } catch (error) {
      toast.error(error || `Failed to ${isEdit ? 'update' : 'create'} job`);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="job-form">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>{isEdit ? 'Edit Job' : 'Create New Job'}</h2>
        <button
          className="btn btn-outline-secondary"
          onClick={() => navigate('/jobs')}
        >
          Cancel
        </button>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="row g-3">
              {/* Job Number */}
              <div className="col-md-6">
                <label className="form-label">Job Number</label>
                <input
                  type="text"
                  className="form-control"
                  name="job_number"
                  value={formData.job_number}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* Well Name */}
              <div className="col-md-6">
                <label className="form-label">Well Name</label>
                <input
                  type="text"
                  className="form-control"
                  name="well_name"
                  value={formData.well_name}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* Status */}
              <div className="col-md-6">
                <label className="form-label">Status</label>
                <select
                  className="form-select"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  required
                >
                  <option value="PLANNED">Planned</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                  <option value="ON_HOLD">On Hold</option>
                  <option value="CANCELLED">Cancelled</option>
                </select>
              </div>

              {/* Spud Date */}
              <div className="col-md-6">
                <label className="form-label">Spud Date</label>
                <input
                  type="date"
                  className="form-control"
                  name="spud_date"
                  value={formData.spud_date}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* Field */}
              <div className="col-md-6">
                <label className="form-label">Field</label>
                <input
                  type="text"
                  className="form-control"
                  name="field"
                  value={formData.field}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* Country */}
              <div className="col-md-6">
                <label className="form-label">Country</label>
                <input
                  type="text"
                  className="form-control"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  required
                />
              </div>

              {/* Rig Name */}
              <div className="col-md-6">
                <label className="form-label">Rig Name</label>
                <input
                  type="text"
                  className="form-control"
                  name="rig_name"
                  value={formData.rig_name}
                  onChange={handleChange}
                />
              </div>

              {/* Operator */}
              <div className="col-md-6">
                <label className="form-label">Operator</label>
                <input
                  type="text"
                  className="form-control"
                  name="operator"
                  value={formData.operator}
                  onChange={handleChange}
                />
              </div>

              {/* Total Depth */}
              <div className="col-md-6">
                <label className="form-label">Total Depth (ft)</label>
                <input
                  type="number"
                  className="form-control"
                  name="total_depth"
                  value={formData.total_depth}
                  onChange={handleChange}
                />
              </div>

              {/* Well Type */}
              <div className="col-md-6">
                <label className="form-label">Well Type</label>
                <input
                  type="text"
                  className="form-control"
                  name="well_type"
                  value={formData.well_type}
                  onChange={handleChange}
                />
              </div>

              {/* Description */}
              <div className="col-12">
                <label className="form-label">Description</label>
                <textarea
                  className="form-control"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows="3"
                />
              </div>

              {/* Submit Button */}
              <div className="col-12">
                <button type="submit" className="btn btn-primary">
                  {isEdit ? 'Update Job' : 'Create Job'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default JobForm;