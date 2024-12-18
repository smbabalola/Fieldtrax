// JobSidebar.jsx
import React, { useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Nav, Spinner, Badge } from 'react-bootstrap';
import { 
  fetchJobDetails,
  selectSelectedJob,
  selectJobDetailsLoading,
  selectJobDetailsError
} from '../store/slices/jobsSlice';

const JobSidebar = () => {
  const { jobId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  
  const job = useSelector(selectSelectedJob);
  const loading = useSelector(selectJobDetailsLoading);
  const error = useSelector(selectJobDetailsError);

  useEffect(() => {
    if (jobId) {
      dispatch(fetchJobDetails(jobId));
    }
  }, [dispatch, jobId]);

  // Get current active path for navigation
  const currentPath = location.pathname.split(`/jobs/${jobId}/`)[1] || '';

  // Status badge styling
  const getStatusBadgeVariant = (status) => {
    const variants = {
      PENDING: 'warning',
      IN_PROGRESS: 'primary',
      COMPLETED: 'success',
      CANCELLED: 'danger',
      default: 'secondary'
    };
    return variants[status] || variants.default;
  };

  const navItems = [
    { path: '', label: 'Overview', icon: 'bi-house' },
    { path: 'well', label: 'Well Information', icon: 'bi-diagram-3' },
    { path: 'logs', label: 'Job Logs', icon: 'bi-journal-text' },
    { path: 'fluids', label: 'Fluids', icon: 'bi-droplet' },
    { path: 'barriers', label: 'Physical Barriers', icon: 'bi-shield' },
    { path: 'tally', label: 'Tally', icon: 'bi-list-ol' },
    { path: 'backload', label: 'Backload', icon: 'bi-box-seam' },
    { path: 'tickets', label: 'Service Tickets', icon: 'bi-receipt' },
    { path: 'purchase-orders', label: 'Purchase Orders', icon: 'bi-cart' }
  ];

  if (loading) {
    return (
      <div className="border-end bg-white" style={{ width: 280 }}>
        <div className="d-flex justify-content-center align-items-center" style={{ height: 200 }}>
          <Spinner animation="border" role="status" variant="primary">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="border-end bg-white" style={{ width: 280 }}>
        <div className="alert alert-danger m-3">
          <i className="bi bi-exclamation-triangle-fill me-2"></i>
          {error}
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="border-end bg-white" style={{ width: 280 }}>
        <div className="text-center p-4">
          <i className="bi bi-folder2-open display-6 text-muted mb-3"></i>
          <p className="text-muted">No job details available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="border-end bg-white" style={{ width: 280 }}>
      {/* Job Header */}
      <div className="p-3 border-bottom">
        <div className="d-flex justify-content-between align-items-start mb-2">
          <div>
            <h6 className="text-muted mb-1">Job Number</h6>
            <h5 className="mb-0">{job.job_number}</h5>
          </div>
          <Badge bg={getStatusBadgeVariant(job.status)}>
            {job.status?.replace('_', ' ')}
          </Badge>
        </div>
        <div className="small text-muted mt-2">
          <div><strong>Well:</strong> {job.well?.name}</div>
          <div><strong>Rig:</strong> {job.rig?.rig_name}</div>
          <div><strong>Operator:</strong> {job.operator?.name}</div>
        </div>
      </div>

      {/* Navigation */}
      <Nav className="flex-column p-2">
        {navItems.map(item => (
          <Nav.Link
            key={item.path}
            onClick={() => navigate(`/jobs/${jobId}/${item.path}`)}
            className={`d-flex align-items-center py-2 px-3 ${
              currentPath === item.path ? 'active bg-light rounded' : 'text-body'
            }`}
          >
            <i className={`${item.icon} me-3`}></i>
            {item.label}
            {/* Optional: Add counters or status indicators */}
            {item.path === 'logs' && job.logs_count > 0 && (
              <Badge bg="primary" pill className="ms-auto">
                {job.logs_count}
              </Badge>
            )}
            {item.path === 'tickets' && job.tickets_count > 0 && (
              <Badge bg="primary" pill className="ms-auto">
                {job.tickets_count}
              </Badge>
            )}
          </Nav.Link>
        ))}
      </Nav>

      {/* Job Timeline (Optional) */}
      <div className="border-top p-3">
        <h6 className="text-muted mb-2">Timeline</h6>
        <div className="small">
          <div className="mb-1">
            <i className="bi bi-calendar-event me-2"></i>
            Started: {new Date(job.start_date).toLocaleDateString()}
          </div>
          {job.end_date && (
            <div>
              <i className="bi bi-calendar-check me-2"></i>
              Ended: {new Date(job.end_date).toLocaleDateString()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobSidebar;