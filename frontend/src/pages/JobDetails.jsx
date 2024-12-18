import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useJobs from '../hooks/useJobs';
import { Tab, Nav, Card, Button, Badge } from 'react-bootstrap';
import LoadingSpinner from '../components/common/LoadingSpinner';

const JobDetails = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const { selectedJob, loading, error, loadJobDetails } = useJobs();

  useEffect(() => {
    if (jobId) {
      loadJobDetails(jobId);
    }
  }, [jobId, loadJobDetails]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="alert alert-danger">
        Error loading job details: {error}
      </div>
    );
  }

  if (!selectedJob) {
    return (
      <div className="alert alert-info">
        Job not found
      </div>
    );
  }

  return (
    <div className="job-details">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">Job: {selectedJob.job_number}</h2>
          <p className="text-muted mb-0">
            {selectedJob.well_name} - {selectedJob.field}, {selectedJob.country}
          </p>
        </div>
        <div>
          <Button 
            variant="outline-secondary" 
            className="me-2"
            onClick={() => navigate(-1)}
          >
            Back
          </Button>
          <Button variant="primary">Edit Job</Button>
        </div>
      </div>

      {/* Status Cards */}
      <div className="row g-4 mb-4">
        <div className="col-md-3">
          <Card className="border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Status</h6>
              <Badge bg={
                selectedJob.status === 'Active' ? 'success' :
                selectedJob.status === 'Planned' ? 'primary' :
                selectedJob.status === 'Completed' ? 'info' :
                'secondary'
              }>
                {selectedJob.status}
              </Badge>
            </Card.Body>
          </Card>
        </div>
        <div className="col-md-3">
          <Card className="border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Spud Date</h6>
              <p className="mb-0">{new Date(selectedJob.spud_date).toLocaleDateString()}</p>
            </Card.Body>
          </Card>
        </div>
        <div className="col-md-3">
          <Card className="border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Measured Depth</h6>
              <p className="mb-0">{selectedJob.measured_depth || 'N/A'}</p>
            </Card.Body>
          </Card>
        </div>
        <div className="col-md-3">
          <Card className="border-0 shadow-sm">
            <Card.Body>
              <h6 className="text-muted">Total Vertical Depth</h6>
              <p className="mb-0">{selectedJob.total_vertical_depth || 'N/A'}</p>
            </Card.Body>
          </Card>
        </div>
      </div>

      {/* Tab Navigation */}
      <Tab.Container defaultActiveKey="overview">
        <Card className="border-0 shadow-sm">
          <Card.Header className="bg-white">
            <Nav variant="tabs" className="border-bottom-0">
              <Nav.Item>
                <Nav.Link eventKey="overview">Overview</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="well">Well Information</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="fluids">Fluids</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="reports">Reports</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="logs">Job Logs</Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Header>
          <Card.Body>
            <Tab.Content>
              <Tab.Pane eventKey="overview">
                <div className="row">
                  <div className="col-md-6">
                    <h5>Job Information</h5>
                    <table className="table">
                      <tbody>
                        <tr>
                          <th>Job Center</th>
                          <td>{selectedJob.jobcenter_id}</td>
                        </tr>
                        <tr>
                          <th>Operator</th>
                          <td>{selectedJob.operator_id}</td>
                        </tr>
                        <tr>
                          <th>Rig</th>
                          <td>{selectedJob.rig_id}</td>
                        </tr>
                        <tr>
                          <th>Service Code</th>
                          <td>{selectedJob.service_code}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div className="col-md-6">
                    <h5>Dates</h5>
                    <table className="table">
                      <tbody>
                        <tr>
                          <th>Spud Date</th>
                          <td>{new Date(selectedJob.spud_date).toLocaleDateString()}</td>
                        </tr>
                        <tr>
                          <th>Mobilization Date</th>
                          <td>
                            {selectedJob.mobilization_date ? 
                              new Date(selectedJob.mobilization_date).toLocaleDateString() : 
                              'N/A'}
                          </td>
                        </tr>
                        <tr>
                          <th>Demobilization Date</th>
                          <td>
                            {selectedJob.demobilization_date ? 
                              new Date(selectedJob.demobilization_date).toLocaleDateString() : 
                              'N/A'}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </Tab.Pane>
              <Tab.Pane eventKey="well">
                {/* Add Well Information Component */}
                <p>Well information content will go here</p>
              </Tab.Pane>
              <Tab.Pane eventKey="fluids">
                {/* Add Fluids Component */}
                <p>Fluids content will go here</p>
              </Tab.Pane>
              <Tab.Pane eventKey="reports">
                {/* Add Reports Component */}
                <p>Reports content will go here</p>
              </Tab.Pane>
              <Tab.Pane eventKey="logs">
                {/* Add Job Logs Component */}
                <p>Job logs content will go here</p>
              </Tab.Pane>
            </Tab.Content>
          </Card.Body>
        </Card>
      </Tab.Container>
    </div>
  );
};

export default JobDetails;