// File: /src/pages/job/CreateJobPage.jsx
import React, { useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Card, Alert, Row, Col, Nav, Tab, Button } from 'react-bootstrap';
import { 
  createJob, 
  selectJobsLoading, 
  selectJobsError,
  fetchRelatedData
} from '../../store/slices/jobsSlice';
import NavigationButtons from '../../components/common/NavigationButtons';
import CustomerInfoTab from "../../components/jobs/CreateJob/tabs/CustomerInfoTab";
import WellInfoTab from '../../components/jobs/CreateJob/tabs/WellInfoTab';
import RigInfoTab from '../../components/jobs/CreateJob/tabs/RigInfoTab';
import WellboreGeometryTab from '../../components/jobs/CreateJob/tabs/WellboreGeometryTab';
import TrajectoryTab from '../../components/jobs/CreateJob/tabs/TrajectoryTab';
import FluidsTab from '../../components/jobs/CreateJob/tabs/FluidsTab';
import { toast } from 'react-toastify';

const INITIAL_FORM_DATA = {
  operator_id: '',
  job_name: '',
  job_center_id: '',
  job_description: '',
  service_code: '',
  country: '',
  purchase_order_id: '',
  well_id: '',
  field_name: '',
  well_type: '',
  well_status: '',
  rig_id: '',
  rig_type: '',
  rig_capability: '',
  rig_status: '',
};

const TABS = [
  {
    id: 'customer-info',
    title: 'Customer Information',
    component: CustomerInfoTab,
    requiredFields: ['operator_id', 'job_name', 'job_description', 'job_center_id']
  },
  {
    id: 'well-info',
    title: 'Well Information',
    component: WellInfoTab,
    requiredFields: ['well_id', 'field_name', 'well_type']
  },
  {
    id: 'rig-info',
    title: 'Rig Information',
    component: RigInfoTab,
    requiredFields: ['rig_id', 'rig_type']
  },
  {
    id: 'wellbore-geometry',
    title: 'Wellbore Geometry',
    component: WellboreGeometryTab,
    requiredFields: ['wellbore_type', 'total_depth']
  },
  {
    id: 'trajectory',
    title: 'Trajectory',
    component: TrajectoryTab,
    requiredFields: ['trajectory_type']
  },
  {
    id: 'fluids',
    title: 'Fluids',
    component: FluidsTab,
    requiredFields: ['primary_fluid_type']
  }
];

const CreateJobPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(TABS[0].id);
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [formErrors, setFormErrors] = useState({});
  const [error, setError] = useState(null);

  const isLoading = useSelector(selectJobsLoading);
  const apiError = useSelector(selectJobsError);

  // Check if current tab is valid
  const isTabValid = useCallback((tabId) => {
    const tab = TABS.find(t => t.id === tabId);
    if (!tab) return true;

    return tab.requiredFields.every(field => {
      const value = formData[field];
      return value !== undefined && value !== null && value !== '';
    });
  }, [formData]);

  // Handle form data changes
  const handleFormChange = useCallback((data) => {
    console.log('Form data being updated:', data);
    setFormData(prevData => {
      const newData = {
        ...prevData,
        ...data
      };
      console.log('Updated form data:', newData);
      return newData;
    });
    setFormErrors({});
  }, []);

  // Handle tab change
  const handleTabChange = useCallback((tabId) => {
    const currentTabValid = isTabValid(activeTab);
    if (!currentTabValid) {
      const tab = TABS.find(t => t.id === activeTab);
      const missingFields = tab.requiredFields.filter(field => !formData[field]);
      setError(`Please complete these required fields: ${missingFields.join(', ')}`);
      return;
    }
    setActiveTab(tabId);
    setError(null);
  }, [activeTab, formData, isTabValid]);

  // Navigation handlers
  const handlePrevious = useCallback(() => {
    const currentIndex = TABS.findIndex(tab => tab.id === activeTab);
    if (currentIndex > 0) {
      setActiveTab(TABS[currentIndex - 1].id);
      setError(null);
    }
  }, [activeTab]);

  const handleNext = useCallback(() => {
    const currentIndex = TABS.findIndex(tab => tab.id === activeTab);
    const currentTabValid = isTabValid(activeTab);
    
    if (currentTabValid && currentIndex < TABS.length - 1) {
      setActiveTab(TABS[currentIndex + 1].id);
      setError(null);
    } else if (!currentTabValid) {
      const tab = TABS[currentIndex];
      const missingFields = tab.requiredFields.filter(field => !formData[field]);
      setError(`Please complete these required fields: ${missingFields.join(', ')}`);
    }
  }, [activeTab, formData, isTabValid]);

  // Save handler
  const handleSave = useCallback(async () => {
    const invalidTabs = TABS.filter(tab => !isTabValid(tab.id));
    if (invalidTabs.length > 0) {
      const missingFieldsList = invalidTabs
        .map(tab => `${tab.title}: ${tab.requiredFields.filter(field => !formData[field]).join(', ')}`)
        .join('\n');
      setError(`Please complete all required fields:\n${missingFieldsList}`);
      return;
    }

    try {
      const result = await dispatch(createJob(formData)).unwrap();
      toast.success('Job created successfully');
      navigate(`/jobs/${result.id}`);
    } catch (err) {
      setError(err.message || 'Failed to create job');
      toast.error(err.message || 'Failed to create job');
    }
  }, [dispatch, formData, isTabValid, navigate]);

  return (
    <div className="p-4">
      <Card>
        <Card.Header className="d-flex justify-content-between align-items-center">
          <h4 className="mb-0">Create New Job</h4>
          <Button variant="outline-primary" onClick={() => navigate('/jobs')}>
            Back to Jobs
          </Button>
        </Card.Header>
        <Card.Body>
          {(error || apiError) && (
            <Alert variant="danger" onClose={() => setError(null)} dismissible>
              {error || apiError}
            </Alert>
          )}

          <Tab.Container activeKey={activeTab}>
            <Row>
              <Col md={3}>
                <Nav variant="pills" className="flex-column">
                  {TABS.map((tab) => (
                    <Nav.Item key={tab.id}>
                      <Nav.Link
                        eventKey={tab.id}
                        onClick={() => handleTabChange(tab.id)}
                        className="d-flex align-items-center"
                      >
                        {tab.title}
                        {isTabValid(tab.id) && (
                          <i className="bi bi-check-circle-fill text-success ms-2"></i>
                        )}
                      </Nav.Link>
                    </Nav.Item>
                  ))}
                </Nav>
              </Col>
              <Col md={9}>
                <Tab.Content>
                  <Tab.Pane eventKey={activeTab}>
                    {React.createElement(TABS.find(tab => tab.id === activeTab)?.component, {
                      data: formData,
                      onChange: handleFormChange,
                      errors: formErrors
                    })}
                  </Tab.Pane>
                </Tab.Content>

                <div className="mt-4 border-top pt-3">
                  <NavigationButtons
                    onPrevious={handlePrevious}
                    onNext={handleNext}
                    onSave={handleSave}
                    canGoNext={isTabValid(activeTab)}
                    canGoPrevious={TABS.findIndex(tab => tab.id === activeTab) > 0}
                    canSave={TABS.every(tab => isTabValid(tab.id))}
                    isLastStep={activeTab === TABS[TABS.length - 1].id}
                    isLoading={isLoading}
                  />
                </div>
              </Col>
            </Row>
          </Tab.Container>
        </Card.Body>
      </Card>
    </div>
  );
};

export default CreateJobPage;