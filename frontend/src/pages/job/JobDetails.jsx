// File: /frontend/src/pages/jobs/JobDetails.jsx
import React, { useState, useEffect } from 'react';
import { Card, Tab, Nav, Spinner, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';

const JobDetailsHeader = ({ job }) => {
  if (!job) return null;
  
  return (
    <Card className="mb-4 shadow-sm">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <h4 className="mb-1">{job.jobName}</h4>
            <p className="text-muted mb-0">
              {job.operator} • {job.wellName} • {job.field}, {job.country}
            </p>
          </div>
          <div className="text-end">
            <span className={`badge bg-${job.status === 'active' ? 'success' : 'secondary'}`}>
              {job.status}
            </span>
          </div>
        </div>
      </Card.Body>
    </Card>
  );
};

const LoadingSpinner = () => (
  <div className="text-center p-5">
    <Spinner animation="border" role="status" variant="primary">
      <span className="visually-hidden">Loading...</span>
    </Spinner>
  </div>
);

const JobDetails = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('jobInfo');
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJobDetails = async () => {
      try {
        setLoading(true);
        // TODO: Replace with actual API call
        // const response = await jobService.getJobById(jobId);
        // setJob(response.data);
        
        // Temporary mock data
        setTimeout(() => {
          setJob({
            jobName: 'Test Job',
            operator: 'Test Operator',
            wellName: 'Test Well',
            field: 'Test Field',
            country: 'Test Country',
            status: 'active'
          });
          setLoading(false);
        }, 1000);
      } catch (err) {
        setError(err.message || 'Failed to fetch job details');
        setLoading(false);
      }
    };

    if (jobId) {
      fetchJobDetails();
    }
  }, [jobId]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <Alert variant="danger">
        <Alert.Heading>Error Loading Job Details</Alert.Heading>
        <p>{error}</p>
        <div className="d-flex justify-content-end">
          <button 
            className="btn btn-outline-danger"
            onClick={() => navigate('/dashboard')}
          >
            Back to Dashboard
          </button>
        </div>
      </Alert>
    );
  }

  if (!job) {
    return (
      <Alert variant="warning">
        <Alert.Heading>Job Not Found</Alert.Heading>
        <p>The requested job could not be found.</p>
        <div className="d-flex justify-content-end">
          <button 
            className="btn btn-outline-warning"
            onClick={() => navigate('/dashboard')}
          >
            Back to Dashboard
          </button>
        </div>
      </Alert>
    );
  }

  return (
    <div className="job-details">
      <JobDetailsHeader job={job} />
      
      <Card className="shadow-sm">
        <Card.Header className="bg-white">
          <Nav 
            variant="tabs" 
            className="flex-nowrap overflow-auto hide-scrollbar border-bottom-0"
            style={{ marginBottom: '-0.5rem' }}
          >
            <Nav.Item>
              <Nav.Link 
                active={activeTab === 'jobInfo'}
                onClick={() => setActiveTab('jobInfo')}
              >
                Job Info
              </Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link 
                active={activeTab === 'wellInfo'}
                onClick={() => setActiveTab('wellInfo')}
              >
                Well Info
              </Nav.Link>
            </Nav.Item>
            {/* ... rest of the tabs ... */}
          </Nav>
        </Card.Header>

        <Card.Body className="p-4">
          {activeTab === 'jobInfo' && (
            <div>Job Info Content</div>
          )}
          {activeTab === 'wellInfo' && (
            <div>Well Info Content</div>
          )}
          {/* ... rest of the tab content ... */}
        </Card.Body>
      </Card>

      <style>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
};

export default JobDetails;