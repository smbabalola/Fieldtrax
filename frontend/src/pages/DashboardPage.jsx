// src/pages/DashboardPage.jsx
import React, { useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { 
  fetchJobs, 
  setPage,
  setSorting,
  setFilter,
  resetFilters,
  selectJobs, 
  selectJobsLoading, 
  selectJobsError,
  selectJobsPagination,
  selectJobsSorting,
  selectJobsFilters,
} from '../store/slices/jobsSlice';
import { openCreateJobModal } from '../store/slices/uiSlice';
import JobsTable from '../components/jobs/JobsTable';
import JobFilters from '../components/jobs/JobFilters';
import CreateJobModal from '../components/jobs/CreateJobModal';
import * as jobService from '../services/jobService';

// StatCard Component remains the same
const StatCard = ({ title, count, variant = 'primary', icon }) => (
  <Col md={3} className="mb-4">
    <Card className={`border-0 bg-${variant} bg-opacity-10 h-100`}>
      <Card.Body>
        <div className="d-flex align-items-center">
          {icon && <div className={`text-${variant} me-3`}>
            <i className={`bi ${icon} fs-1`}></i>
          </div>}
          <div>
            <div className="text-muted small">{title}</div>
            <h3 className="mb-0">{count || 0}</h3>
          </div>
        </div>
      </Card.Body>
    </Card>
  </Col>
);

const DashboardPage = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  // Redux selectors
  const jobs = useSelector(selectJobs);
  const loading = useSelector(selectJobsLoading);
  const error = useSelector(selectJobsError);
  const pagination = useSelector(selectJobsPagination);
  const sorting = useSelector(selectJobsSorting);
  const filters = useSelector(selectJobsFilters);

  // Calculate stats
  const stats = useMemo(() => {
    if (!Array.isArray(jobs)) return { active: 0, planned: 0, completed: 0, total: 0 };
    
    return {
      active: jobs.filter(job => job.status?.toLowerCase() === 'active').length,
      planned: jobs.filter(job => job.status?.toLowerCase() === 'planned').length,
      completed: jobs.filter(job => job.status?.toLowerCase() === 'completed').length,
      total: jobs.length
    };
  }, [jobs]);

  // Fetch jobs data
  const fetchJobsData = async () => {
    try {
      const response = await dispatch(fetchJobs({
        page: pagination.currentPage,
        pageSize: pagination.pageSize,
        sortField: sorting.field,
        sortOrder: sorting.direction,
        status: filters.status,
        searchTerm: filters.searchTerm
      })).unwrap();
  
      if (!response?.items) {
        throw new Error('Invalid jobs data format');
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
      if (err.message === 'Authentication required') {
        navigate('/login');
      } else {
        toast.error(err.message || 'Failed to fetch jobs');
      }
    }
  };

  // Initial fetch and cleanup
  useEffect(() => {
    fetchJobsData();
  }, [pagination.currentPage, pagination.pageSize, sorting, filters]);

  // Error handling
  useEffect(() => {
    if (error) {
      toast.error(typeof error === 'string' ? error : 'An error occurred loading jobs');
    }
  }, [error]);

  // Event Handlers
  const handlePageChange = (newPage) => {
    dispatch(setPage(newPage));
  };

  const handleSort = (newSorting) => {
    dispatch(setSorting(newSorting));
  };

  const handleFilterChange = (newFilters) => {
    dispatch(setFilter(newFilters));
  };

  const handleCreateJob = () => {
    dispatch(openCreateJobModal());
  };

  // Bulk action handlers
  const handleBulkStatusChange = async (status, selectedJobs) => {
    try {
      await Promise.all(
        selectedJobs.map(jobId => 
          jobService.update(jobId, { status })
        )
      );
      toast.success(`Successfully updated ${selectedJobs.length} jobs to ${status}`);
      fetchJobsData();
    } catch (err) {
      console.error('Bulk status update error:', err);
      toast.error('Failed to update job statuses');
    }
  };

  const handleBulkExport = async (selectedJobs) => {
    try {
      const response = await jobService.export(selectedJobs);
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `jobs-export-${new Date().toISOString()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success('Jobs exported successfully');
    } catch (err) {
      console.error('Export error:', err);
      toast.error('Failed to export jobs');
    }
  };

  const handleBulkDelete = async (selectedJobs) => {
    if (!window.confirm(`Are you sure you want to delete ${selectedJobs.length} jobs?`)) {
      return;
    }

    try {
      await Promise.all(
        selectedJobs.map(jobId => 
          jobService.delete(jobId)
        )
      );
      toast.success(`Successfully deleted ${selectedJobs.length} jobs`);
      fetchJobsData();
    } catch (err) {
      console.error('Bulk delete error:', err);
      toast.error('Failed to delete jobs');
    }
  };

  return (
    <Container fluid className="py-4">
      {/* Stats Section */}
      <Row>
        <StatCard 
          title="Active Jobs" 
          count={stats.active} 
          variant="success"
          icon="bi-play-circle"
        />
        <StatCard 
          title="Planned Jobs" 
          count={stats.planned} 
          variant="warning"
          icon="bi-calendar-event"
        />
        <StatCard 
          title="Completed Jobs" 
          count={stats.completed} 
          variant="info"
          icon="bi-check-circle"
        />
        <StatCard 
          title="Total Jobs" 
          count={stats.total} 
          variant="primary"
          icon="bi-folder"
        />
      </Row>

      {/* Jobs Table Section */}
      <Row>
        <Col>
          <Card className="shadow-sm">
            <Card.Header className="bg-white py-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0">
                  <i className="bi bi-list-task me-2"></i>
                  Jobs Management
                </h5>
                <div>
                  <button 
                    className="btn btn-primary"
                    onClick={handleCreateJob}
                    disabled={loading}
                  >
                    <i className="bi bi-plus-circle me-2"></i>
                    Create Job
                  </button>
                </div>
              </div>
            </Card.Header>
            <Card.Body className="p-0">
              {jobs.length > 0 && (
                <div className="p-3 border-bottom">
                  <JobFilters
                    filters={filters}
                    loading={loading}
                    onChange={handleFilterChange}
                    onReset={() => dispatch(resetFilters())}
                  />
                </div>
              )}
              
              <JobsTable 
                jobs={jobs}
                loading={loading}
                error={error}
                pagination={pagination}
                sorting={sorting}
                filters={filters}
                onSort={handleSort}
                onPageChange={handlePageChange}
                onFilterChange={handleFilterChange}
                onBulkStatusChange={handleBulkStatusChange}
                onBulkExport={handleBulkExport}
                onBulkDelete={handleBulkDelete}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Create Job Modal */}
      <CreateJobModal />
    </Container>
  );
};

export default DashboardPage;