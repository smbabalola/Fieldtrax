// src/components/jobs/JobsTable.jsx
import React, { useMemo, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Table, Badge, Button, Spinner } from 'react-bootstrap';
import { 
  openJobDetailsModal, 
  setJobDetailsLoading, 
  setJobDetailsError,
  openCreateJobModal,
  selectTableColumns 
} from '../../store/slices/uiSlice';
import jobService from '../../services/jobService';
import JobDetailsModal from './JobDetailsModal';
import CreateJobModal from './CreateJobModal';
import './JobsTable.css';

const columnRenderers = {
  job_name: (job) => (
    <div>
      <div className="fw-bold">{job.job_name}</div>
      <small className="text-muted">Center: {job.job_center?.job_center_name || 'N/A'}</small>
    </div>
  ),
  status: (job) => (
    <Badge bg={getStatusColor(job.status)}>
      {job.status}
    </Badge>
  ),
  well: (job) => (
    <div>
      <div className="fw-bold">{job.well?.well_name || 'N/A'}</div>
      <small className="text-muted">
        API: {job.well?.api_number || 'N/A'} | MD: {job.measured_depth || 'N/A'} | TVD: {job.total_vertical_depth || 'N/A'}
      </small>
    </div>
  ),
  operator: (job) => (
    <div>
      <div>{job.operator?.operator_name || 'N/A'}</div>
      <small className="text-muted">
        {job.operator?.company_code || 'N/A'} - {job.service_code || 'No Code'}
      </small>
    </div>
  ),
  rig: (job) => (
    <div>
      <div>{job.rig?.rig_name || 'N/A'}</div>
      <small className="text-muted">
        Water Depth: {job.rig?.water_depth || 'N/A'}m
      </small>
    </div>
  ),
  dates: (job) => {
    const formatDate = (date) => date ? new Date(date).toLocaleDateString() : 'N/A';
    return (
      <div>
        <div>Mob: {formatDate(job.mobilization_date)}</div>
        {job.demobilization_date && (
          <small className="text-muted">
            Demob: {formatDate(job.demobilization_date)}
          </small>
        )}
      </div>
    );
  }
};

const getStatusColor = (status) => {
  const statusColors = {
    'Active': 'success',
    'Planned': 'warning',
    'Completed': 'info',
    'Cancelled': 'danger',
    'In Progress': 'primary'
  };
  return statusColors[status] || 'secondary';
};

const JobsTable = ({
  jobs = [],
  loading = false,
  error = null,
  pagination = {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0
  },
  onPageChange,
  onSort
}) => {
  const dispatch = useDispatch();
  const columns = useSelector(selectTableColumns);
  const [selectedJobs, setSelectedJobs] = React.useState([]);

  const handleRowClick = async (job) => {
    try {
      dispatch(setJobDetailsLoading(true));
      const response = await jobService.getJob(job.id);
      dispatch(openJobDetailsModal(response));
    } catch (error) {
      console.error('Error fetching job details:', error);
      dispatch(setJobDetailsError(error.message));
    }
  };

  const handleCreateJob = () => {
    dispatch(openCreateJobModal());
  };

  const visibleColumns = useMemo(() => {
    return Object.entries(columns)
      .filter(([, config]) => config.visible)
      .sort(([, a], [, b]) => a.order - b.order)
      .map(([columnId, config]) => ({
        id: columnId,
        ...config,
        render: columnRenderers[columnId] || (job => String(job[columnId] || 'N/A'))
      }));
  }, [columns]);

  const handleSelectJob = (jobId) => {
    setSelectedJobs(prev => 
      prev.includes(jobId)
        ? prev.filter(id => id !== jobId)
        : [...prev, jobId]
    );
  };

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="table-container">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <Button 
          variant="primary"
          onClick={handleCreateJob}
        >
          <i className="bi bi-plus-lg me-2"></i>
          Create New Job
        </Button>
      </div>

      <Table hover bordered className="align-middle">
        <thead>
          <tr>
            <th style={{ width: '40px' }}>
              <input
                type="checkbox"
                checked={selectedJobs.length === jobs.length && jobs.length > 0}
                onChange={(e) => {
                  setSelectedJobs(e.target.checked ? jobs.map(job => job.id) : []);
                }}
              />
            </th>
            {visibleColumns.map((column) => (
              <th 
                key={column.id}
                style={{ width: column.width }}
                onClick={() => onSort?.(column.id)}
                className="cursor-pointer"
              >
                {column.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={visibleColumns.length + 1} className="text-center py-4">
                <Spinner animation="border" role="status">
                  <span className="visually-hidden">Loading...</span>
                </Spinner>
              </td>
            </tr>
          ) : jobs.length === 0 ? (
            <tr>
              <td colSpan={visibleColumns.length + 1} className="text-center py-4">
                No jobs found
              </td>
            </tr>
          ) : (
            jobs.map(job => (
              <tr 
                key={job.id}
                onClick={() => handleRowClick(job)}
                className="table-row hover-bg"
              >
                <td onClick={e => e.stopPropagation()}>
                  <input
                    type="checkbox"
                    checked={selectedJobs.includes(job.id)}
                    onChange={(e) => {
                      e.stopPropagation();
                      handleSelectJob(job.id);
                    }}
                  />
                </td>
                {visibleColumns.map((column) => (
                  <td key={column.id} style={{ width: column.width }}>
                    {column.render(job)}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </Table>

      <JobDetailsModal />
      <CreateJobModal />
    </div>
  );
};

export default JobsTable;