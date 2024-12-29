import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Card, Modal, Spinner, Alert, Tab, Nav } from 'react-bootstrap';
import JobInfoTab from './tabs/JobInfoTab';

const JobDetailModal = ({ 
  show, 
  onHide, 
  jobId, 
  onJobUpdate,
  initialTab = 'jobInfo' 
}) => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [job, setJob] = useState(null);
  const [activeTab, setActiveTab] = useState(initialTab);

  useEffect(() => {
    const fetchJobDetails = async () => {
      if (!jobId || !show) return;
      
      try {
        setLoading(true);
        setError(null);
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

    fetchJobDetails();
  }, [jobId, show, dispatch]);

  const handleSave = async (updatedData) => {
    try {
      // TODO: Implement actual API call
      console.log('Updating job:', updatedData);
      setJob(prev => ({
        ...prev,
        ...updatedData
      }));
      onJobUpdate?.(updatedData);
    } catch (error) {
      console.error('Error updating job:', error);
      // TODO: Add error handling
    }
  };

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
    <Modal 
      show={show} 
      onHide={onHide}
      size="xl"
      fullscreen="lg-down"
      backdrop="static"
      className="job-detail-modal"
    >
      <Modal.Header closeButton>
        <Modal.Title>
          {job?.jobName || 'Job Details'}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body className="p-0">
        {loading ? (
          <div className="text-center p-5">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          </div>
        ) : error ? (
          <Alert variant="danger" className="m-3">
            <Alert.Heading>Error Loading Job Details</Alert.Heading>
            <p>{error}</p>
          </Alert>
        ) : !job ? (
          <Alert variant="warning" className="m-3">
            <Alert.Heading>Job Not Found</Alert.Heading>
            <p>The requested job could not be found.</p>
          </Alert>
        ) : (
          <>
            <Card className="mb-3 border-0">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <h5 className="mb-1">{job.jobNumber}</h5>
                    <p className="text-muted mb-0">
                      {job.operator} • {job.wellName} • {job.field}, {job.country}
                    </p>
                  </div>
                  <span className={`badge bg-${job.status === 'active' ? 'success' : 'secondary'}`}>
                    {job.status}
                  </span>
                </div>
              </Card.Body>
            </Card>

            <Tab.Container activeKey={activeTab} onSelect={setActiveTab}>
              <div className="border-bottom">
                <Nav variant="tabs" className="flex-nowrap overflow-auto hide-scrollbar px-3">
                  {tabs.map(tab => (
                    <Nav.Item key={tab.id}>
                      <Nav.Link eventKey={tab.id}>{tab.label}</Nav.Link>
                    </Nav.Item>
                  ))}
                </Nav>
              </div>

              <Tab.Content className="p-3">
                <Tab.Pane eventKey="jobInfo">
                  <JobInfoTab job={job} onSave={handleSave} />
                </Tab.Pane>
                {activeTab !== 'jobInfo' && (
                  <div className="text-center p-5 text-muted">
                    <h5>Coming Soon</h5>
                    <p>This tab is under development</p>
                  </div>
                )}
              </Tab.Content>
            </Tab.Container>
          </>
        )}
      </Modal.Body>

      <style>{`
        .job-detail-modal .modal-body {
          height: calc(100vh - 120px);
          overflow-y: auto;
        }
        
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </Modal>
  );
};

export default JobDetailModal;