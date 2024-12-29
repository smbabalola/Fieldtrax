// File: /frontend/src/pages/job/JobDetail.jsx
import React, { useState, useEffect } from 'react';
import { Card, Tab, Nav, Spinner, Alert } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import JobInfoTab from './tabs/JobInfoTab';

const JobDetailHeader = ({ job }) => {
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

const JobDetail = () => {
  const { id: jobId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [job, setJob] = useState(null);
  const [activeTab, setActiveTab] = useState('jobInfo');

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
            id: jobId,
            jobName: 'Test Job',
            operator: 'Test Operator',
            wellName: 'Test Well',
            field: 'Test Field',
            country: 'Test Country',
            status: 'active',
            jobNumber: 'JOB-001',
            startDate: '2024-12-18',
            endDate: '2024-12-25',
            description: 'Test job description'
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

  if (loading) return <LoadingSpinner />;

  if (error) {
    return (
      <Alert variant="danger">
        <Alert.Heading>Error Loading Job Details</Alert.Heading>
        <p>{error}</p>
        <div className="d-flex justify-content-end">
          <button 
            className="btn btn-outline-danger"
            onClick={() => navigate('/jobs')}
          >
            Back to Jobs
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
            onClick={() => navigate('/jobs')}
          >
            Back to Jobs
          </button>
        </div>
      </Alert>
    );
  }

  const tabs = [
    { id: 'jobInfo', label: 'Job Info' },
    { id: 'wellInfo', label: 'Well Info' },
    { id: 'linerInfo', label: 'Liner Info' },
    { id: 'fluids', label: 'Fluids' },
    { id: 'calculations', label: 'Calculations' },
    { id: 'tally', label: 'Tally' },
    { id: 'jobLog', label: 'Job Log' },
    { id: 'serviceTickets', label: 'Service Tickets' },
    { id: 'logistics', label: 'Logistics' },
    { id: 'feedback', label: 'Feedback' }
  ];

  return (
    <div className="job-detail">
      <JobDetailHeader job={job} />
      
      <Card className="shadow-sm">
        <Card.Header className="bg-white">
          <Nav 
            variant="tabs" 
            className="flex-nowrap overflow-auto hide-scrollbar border-bottom-0"
            style={{ marginBottom: '-0.5rem' }}
          >
            {tabs.map(tab => (
              <Nav.Item key={tab.id}>
                <Nav.Link 
                  active={activeTab === tab.id}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </Nav.Link>
              </Nav.Item>
            ))}
          </Nav>
        </Card.Header>

        <Card.Body className="p-4">
          {activeTab === 'jobInfo' && (
            <JobInfoTab 
              job={job} 
              onSave={async (updatedData) => {
                try {
                  // TODO: Implement actual API call to update job
                  console.log('Updating job with:', updatedData);
                  // Temporarily update local state
                  setJob(prev => ({
                    ...prev,
                    ...updatedData
                  }));
                } catch (error) {
                  console.error('Error updating job:', error);
                  // TODO: Add error handling
                }
              }}
            />
          )}
          {activeTab !== 'jobInfo' && (
            <div className="text-center p-5 text-muted">
              <h5>Coming Soon</h5>
              <p>This tab is under development</p>
            </div>
          )}
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

export default JobDetail;