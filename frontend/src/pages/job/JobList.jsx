import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Form, InputGroup, Row, Col, Alert, Spinner } from 'react-bootstrap';
import { toast } from 'react-toastify';

const JobList = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    status: '',
    operator: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        setError(null);
        // Mock data for testing
        const mockJobs = [
          {
            id: 1,
            job_name: 'Test Job 1',
            status: 'active',
            operator: 'Operator 1',
            well_name: 'Well 1',
            created_at: '2024-01-01'
          },
          {
            id: 2,
            job_name: 'Test Job 2',
            status: 'completed',
            operator: 'Operator 2',
            well_name: 'Well 2',
            created_at: '2024-01-02'
          }
        ];
        
        setJobs(mockJobs);
      } catch (err) {
        setError('Failed to fetch jobs');
        toast.error('Error loading jobs');
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, [searchTerm, filters]);

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (error) {
    return (
      <Alert variant="danger">
        <Alert.Heading>Error</Alert.Heading>
        <p>{error}</p>
      </Alert>
    );
  }

  return (
    <div className="container-fluid">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Jobs</h2>
        <Button
          variant="primary"
          onClick={() => navigate('/jobs/new')}
        >
          <i className="bi bi-plus-lg me-2"></i>
          New Job
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="mb-4">
        <Card.Body>
          <Row className="g-3">
            <Col md={8}>
              <InputGroup>
                <Form.Control
                  placeholder="Search jobs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button
                  variant="outline-secondary"
                  onClick={() => setShowFilters(!showFilters)}
                >
                  <i className="bi bi-funnel"></i>
                </Button>
              </InputGroup>
            </Col>
          </Row>

          {showFilters && (
            <Row className="mt-3 g-3">
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Status</Form.Label>
                  <Form.Select
                    value={filters.status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                  >
                    <option value="">All Statuses</option>
                    <option value="active">Active</option>
                    <option value="completed">Completed</option>
                    <option value="planned">Planned</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Operator</Form.Label>
                  <Form.Control
                    type="text"
                    value={filters.operator}
                    onChange={(e) => handleFilterChange('operator', e.target.value)}
                    placeholder="Filter by operator"
                  />
                </Form.Group>
              </Col>
            </Row>
          )}
        </Card.Body>
      </Card>

      {/* Jobs Table */}
      <Card>
        <Card.Body className="p-0">
          {loading ? (
            <div className="text-center p-5">
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : jobs.length === 0 ? (
            <div className="text-center p-5">
              <p className="text-muted">No jobs found</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover mb-0">
                <thead>
                  <tr>
                    <th>Job Name</th>
                    <th>Status</th>
                    <th>Operator</th>
                    <th>Well Name</th>
                    <th>Created At</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.map((job) => (
                    <tr key={job.id}>
                      <td>{job.job_name}</td>
                      <td>
                        <span className={`badge bg-${job.status === 'active' ? 'success' : 'secondary'}`}>
                          {job.status}
                        </span>
                      </td>
                      <td>{job.operator}</td>
                      <td>{job.well_name}</td>
                      <td>{new Date(job.created_at).toLocaleDateString()}</td>
                      <td>
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => navigate(`/jobs/${job.id}`)}
                        >
                          View
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};

export default JobList;