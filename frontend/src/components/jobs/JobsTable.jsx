import React, { useState } from 'react';
import { Table, Dropdown, Form, Button, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './JobsTable.css';

const JobsTable = ({ 
  jobs,
  loading,
  error,
  pagination,
  sorting,
  onSort,
  onPageChange,
  onBulkStatusChange,
  onBulkExport,
  onBulkDelete
}) => {
  const [selectedJobs, setSelectedJobs] = useState([]);
  const [selectAll, setSelectAll] = useState(false);

  // Handle select all checkbox
  const handleSelectAll = (e) => {
    setSelectAll(e.target.checked);
    setSelectedJobs(e.target.checked ? jobs.map(job => job.id) : []);
  };

  // Handle individual checkbox
  const handleSelectJob = (e, jobId) => {
    if (e.target.checked) {
      setSelectedJobs([...selectedJobs, jobId]);
    } else {
      setSelectedJobs(selectedJobs.filter(id => id !== jobId));
      setSelectAll(false);
    }
  };

  // Handle sort click
  const handleSortClick = (field) => {
    const newOrder = sorting.field === field && sorting.order === 'asc' ? 'desc' : 'asc';
    onSort({ field, order: newOrder });
  };

  // Render sort icon
  const renderSortIcon = (field) => {
    if (sorting.field !== field) return null;
    return sorting.order === 'asc' ? '↑' : '↓';
  };

  // Handle bulk actions
  const handleBulkAction = (action) => {
    if (selectedJobs.length === 0) return;

    switch (action) {
      case 'export':
        onBulkExport(selectedJobs);
        break;
      case 'delete':
        onBulkDelete(selectedJobs);
        break;
      case 'status':
        // Add your status change logic here
        break;
      default:
        break;
    }
  };

  // Render loading state
  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="alert alert-danger m-3">
        {error}
      </div>
    );
  }

  // Render empty state
  if (!jobs.length) {
    return (
      <div className="text-center py-5 text-muted">
        <i className="bi bi-folder2-open display-4"></i>
        <p className="mt-2">No jobs found</p>
      </div>
    );
  }

  return (
    <div className="table-responsive">
      {selectedJobs.length > 0 && (
        <div className="p-3 bg-light border-bottom">
          <div className="d-flex justify-content-between align-items-center">
            <span>{selectedJobs.length} items selected</span>
            <div>
              <Button
                variant="outline-primary"
                size="sm"
                className="me-2"
                onClick={() => handleBulkAction('export')}
              >
                <i className="bi bi-download me-1"></i> Export
              </Button>
              <Dropdown className="d-inline-block me-2">
                <Dropdown.Toggle variant="outline-primary" size="sm">
                  Change Status
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item onClick={() => onBulkStatusChange('active', selectedJobs)}>
                    Set Active
                  </Dropdown.Item>
                  <Dropdown.Item onClick={() => onBulkStatusChange('completed', selectedJobs)}>
                    Set Completed
                  </Dropdown.Item>
                  <Dropdown.Item onClick={() => onBulkStatusChange('cancelled', selectedJobs)}>
                    Set Cancelled
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
              <Button
                variant="outline-danger"
                size="sm"
                onClick={() => handleBulkAction('delete')}
              >
                <i className="bi bi-trash me-1"></i> Delete
              </Button>
            </div>
          </div>
        </div>
      )}
      
      <Table hover className="mb-0">
        <thead className="bg-light">
          <tr>
            <th className="border-0">
              <Form.Check
                type="checkbox"
                checked={selectAll}
                onChange={handleSelectAll}
              />
            </th>
            <th 
              className="border-0 cursor-pointer"
              onClick={() => handleSortClick('job_name')}
            >
              Job Name {renderSortIcon('job_name')}
            </th>
            <th 
              className="border-0 cursor-pointer"
              onClick={() => handleSortClick('status')}
            >
              Status {renderSortIcon('status')}
            </th>
            <th 
              className="border-0 cursor-pointer"
              onClick={() => handleSortClick('operator')}
            >
              Operator {renderSortIcon('operator')}
            </th>
            <th 
              className="border-0 cursor-pointer"
              onClick={() => handleSortClick('well')}
            >
              Well {renderSortIcon('well')}
            </th>
            <th 
              className="border-0 cursor-pointer"
              onClick={() => handleSortClick('created_at')}
            >
              Created {renderSortIcon('created_at')}
            </th>
            <th className="border-0">Actions</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map(job => (
            <tr key={job.id} className="hover-bg">
              <td>
                <Form.Check
                  type="checkbox"
                  checked={selectedJobs.includes(job.id)}
                  onChange={(e) => handleSelectJob(e, job.id)}
                />
              </td>
              <td>
                <Link to={`/jobs/${job.id}`} className="text-decoration-none">
                  {job.job_name}
                </Link>
              </td>
              <td>
                <span className={`badge bg-${getStatusColor(job.status)}`}>
                  {job.status}
                </span>
              </td>
              <td>{job.operator?.operator_name}</td>
              <td>{job.well?.well_name}</td>
              <td>{formatDate(job.created_at)}</td>
              <td>
                <Dropdown>
                  <Dropdown.Toggle variant="link" size="sm" className="no-caret">
                    <i className="bi bi-three-dots"></i>
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    <Dropdown.Item as={Link} to={`/jobs/${job.id}`}>
                      <i className="bi bi-eye me-2"></i> View Details
                    </Dropdown.Item>
                    <Dropdown.Item as={Link} to={`/jobs/${job.id}/edit`}>
                      <i className="bi bi-pencil me-2"></i> Edit
                    </Dropdown.Item>
                    <Dropdown.Divider />
                    <Dropdown.Item 
                      className="text-danger"
                      onClick={() => onBulkDelete([job.id])}
                    >
                      <i className="bi bi-trash me-2"></i> Delete
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {pagination && (
        <div className="d-flex justify-content-between align-items-center p-3">
          <div>
            Showing {pagination.from} to {pagination.to} of {pagination.total} entries
          </div>
          <div>
            <Button
              variant="outline-primary"
              size="sm"
              className="me-2"
              disabled={!pagination.prevPage}
              onClick={() => onPageChange(pagination.currentPage - 1)}
            >
              Previous
            </Button>
            <Button
              variant="outline-primary"
              size="sm"
              disabled={!pagination.nextPage}
              onClick={() => onPageChange(pagination.currentPage + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to get status color
const getStatusColor = (status) => {
  switch (status?.toLowerCase()) {
    case 'active':
      return 'success';
    case 'planned':
      return 'warning';
    case 'completed':
      return 'info';
    case 'cancelled':
      return 'danger';
    default:
      return 'secondary';
  }
};

// Helper function to format date
const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString();
};

export default JobsTable;