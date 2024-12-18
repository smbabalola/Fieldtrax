// File: /frontend/src/pages/job/JobList.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { 
  fetchJobs, 
  selectJobs,
  selectJobsLoading,
  selectJobsError,
  setFilter,
  setSorting,
  selectJobsFilters,
  selectJobsSorting
} from '../../store/slices/jobsSlice';

const JobList = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const jobs = useSelector(selectJobs);
  const loading = useSelector(selectJobsLoading);
  const error = useSelector(selectJobsError);
  const filters = useSelector(selectJobFilters);
  const sorting = useSelector(selectJobsSorting);

  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const params = {
      ...filters,
      sort_by: sorting.field,
      sort_direction: sorting.direction
    };
    dispatch(fetchJobs(params));
  }, [dispatch, filters, sorting]);

  const handleSort = (field) => {
    const direction = 
      sorting.field === field && sorting.direction === 'asc' 
        ? 'desc' 
        : 'asc';
    dispatch(setSorting({ field, direction }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    dispatch(setFilter({ searchQuery: searchTerm }));
  };

  const renderSortIcon = (field) => {
    if (sorting.field !== field) return null;
    return (
      <i className={`bi bi-sort-${sorting.direction === 'asc' ? 'down' : 'up'} ms-1`}></i>
    );
  };

  const TableHeader = ({ field, children }) => (
    <th 
      scope="col" 
      className="cursor-pointer"
      onClick={() => handleSort(field)}
    >
      <div className="d-flex align-items-center">
        {children}
        {renderSortIcon(field)}
      </div>
    </th>
  );

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-50">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <strong>Error!</strong> {error}
      </div>
    );
  }

  return (
    <div className="container-fluid">
      {/* Header Section */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Jobs List</h2>
        <button
          onClick={() => navigate('/jobs/new')}
          className="btn btn-primary"
        >
          <i className="bi bi-plus-lg me-2"></i>
          Add New Job
        </button>
      </div>

      {/* Search and Filter Section */}
      <div className="mb-4">
        <div className="row g-3">
          <div className="col-md-8">
            <form onSubmit={handleSearch}>
              <div className="input-group">
                <input
                  type="text"
                  className="form-control"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search jobs..."
                />
                <button 
                  type="submit"
                  className="btn btn-outline-secondary"
                >
                  <i className="bi bi-search"></i>
                </button>
              </div>
            </form>
          </div>
          <div className="col-md-4">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn btn-outline-secondary w-100"
            >
              <i className="bi bi-funnel me-2"></i>
              Filters
            </button>
          </div>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="card mt-3">
            <div className="card-body">
              <div className="row g-3">
                <div className="col-md-4">
                  <select
                    value={filters.status || ''}
                    onChange={(e) => dispatch(setFilter({ status: e.target.value }))}
                    className="form-select"
                  >
                    <option value="">All Statuses</option>
                    <option value="Active">Active</option>
                    <option value="Completed">Completed</option>
                    <option value="Planned">Planned</option>
                  </select>
                </div>
                {/* Add more filters as needed */}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Table Section */}
      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <TableHeader field="job_name">Job Number</TableHeader>
                  <TableHeader field="well.well_name">Well</TableHeader>
                  <TableHeader field="operator.operator_name">Operator</TableHeader>
                  <TableHeader field="status">Status</TableHeader>
                  <TableHeader field="rig.rig_name">Rig</TableHeader>
                  <TableHeader field="job_center.job_center_name">Job Center</TableHeader>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(jobs) && jobs.map((job) => (
                  <tr 
                    key={job.id}
                    className="cursor-pointer"
                    onClick={() => navigate(`/jobs/${job.id}`)}
                  >
                    <td>{job.job_name}</td>
                    <td>{job.well?.well_name}</td>
                    <td>{job.operator?.operator_name}</td>
                    <td>
                      <span 
                        className={`badge ${
                          job.status === 'Active' ? 'bg-success' :
                          job.status === 'Completed' ? 'bg-primary' :
                          job.status === 'Planned' ? 'bg-warning' :
                          'bg-secondary'
                        }`}
                      >
                        {job.status}
                      </span>
                    </td>
                    <td>{job.rig?.rig_name}</td>
                    <td>{job.job_center?.job_center_name}</td>
                    <td>
                      <div className="btn-group">
                        <button
                          className="btn btn-sm btn-outline-primary"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/jobs/${job.id}/edit`);
                          }}
                        >
                          <i className="bi bi-pencil me-1"></i>
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-secondary"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/jobs/${job.id}`);
                          }}
                        >
                          <i className="bi bi-eye me-1"></i>
                          View
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
                {(!jobs || jobs.length === 0) && (
                  <tr>
                    <td colSpan="7" className="text-center text-muted py-4">
                      No jobs found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Debug section - only visible during development */}
      {process.env.NODE_ENV === 'development' && jobs && jobs.length > 0 && (
        <div className="mt-4">
          <details>
            <summary>Debug Info</summary>
            <pre className="bg-light p-3">
              {JSON.stringify(jobs[0], null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};

export default JobList;