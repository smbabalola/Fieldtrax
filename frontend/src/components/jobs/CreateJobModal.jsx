// src/components/jobs/CreateJobModal.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Modal, Button, Alert, Spinner } from 'react-bootstrap';
import { createJob } from '../../store/slices/jobsSlice';
import { selectCreateJobModal, closeCreateJobModal } from '../../store/slices/uiSlice';
import JobInfoTab from './CreateJob/tabs/JobInfoTab';
import wellService from '../../services/wellService';
import operatorService from '../../services/operatorService';
import rigService from '../../services/rigService';
import purchaseOrderService from '../../services/purchaseOrderService';
import jobCenterService from '../../services/jobCenterService';

const initialFormData = {
  jobcenter_id: '',
  job_name: '',
  job_description: '',
  operator_id: '',
  service_code: '',
  country: '',
  purchase_order_id: '',
  well_id: '',
  rig_id: '',
  measured_depth: '',
  total_vertical_depth: '',
  spud_date: '',
  status: 'Planned',
  mobilization_date: '',
  demobilization_date: '',
  job_closed: false,
  trainingfile: false
};

const CreateJobModal = () => {
  const dispatch = useDispatch();
  const { isOpen, loading, error } = useSelector(selectCreateJobModal);
  const [formData, setFormData] = useState(initialFormData);
  const [validation, setValidation] = useState({});
  const [referenceData, setReferenceData] = useState({
    wells: [],
    operators: [],
    rigs: [],
    purchaseOrders: [],
    jobCenters: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    if (isOpen) {
      fetchReferenceData();
    }
  }, [isOpen]);

  const fetchReferenceData = async () => {
    try {
      setReferenceData(prev => ({ ...prev, loading: true, error: null }));
      
      const [wellsResponse, operatorsResponse, rigsResponse, purchaseOrdersResponse, jobCentersResponse] = await Promise.all([
        wellService.getWells(),
        operatorService.getOperators(),
        rigService.getAllRigs(),
        purchaseOrderService.getPurchaseOrders(),
        jobCenterService.getJobCenters()
      ]);

      const extractItems = (response) => {
        if (!response) return [];
        if (Array.isArray(response)) return response;
        if (response.items && Array.isArray(response.items)) return response.items;
        if (response.data && Array.isArray(response.data)) return response.data;
        return [];
      };

      setReferenceData({
        wells: extractItems(wellsResponse),
        operators: extractItems(operatorsResponse),
        rigs: extractItems(rigsResponse),
        purchaseOrders: extractItems(purchaseOrdersResponse),
        jobCenters: extractItems(jobCentersResponse),
        loading: false,
        error: null
      });
    } catch (error) {
      console.error('Error fetching reference data:', error);
      setReferenceData(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to load reference data. Please try again.'
      }));
    }
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.job_name) errors.job_name = 'Job name is required';
    if (!formData.jobcenter_id) errors.jobcenter_id = 'Job center is required';
    if (!formData.job_description) errors.job_description = 'Job description is required';
    if (!formData.operator_id) errors.operator_id = 'Operator is required';
    if (!formData.well_id) errors.well_id = 'Well is required';
    
    setValidation(errors);
    return Object.keys(errors).length === 0;
  };

  const handleClose = () => {
    dispatch(closeCreateJobModal());
    setFormData(initialFormData);
    setValidation({});
  };

  const handleDataChange = (updates) => {
    setFormData(prev => ({
      ...prev,
      ...updates
    }));
    
    // Clear validation errors for updated fields
    const updatedFields = Object.keys(updates);
    if (updatedFields.length > 0) {
      setValidation(prev => {
        const newErrors = { ...prev };
        updatedFields.forEach(field => {
          delete newErrors[field];
        });
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      await dispatch(createJob(formData)).unwrap();
      handleClose();
    } catch (err) {
      setValidation(prev => ({
        ...prev,
        submit: err.message || 'Failed to create job'
      }));
    }
  };

  return (
    <Modal show={isOpen} onHide={handleClose} size="xl">
      <Modal.Header closeButton>
        <Modal.Title>Create New Job</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {referenceData.loading ? (
          <div className="text-center py-4">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          </div>
        ) : (
          <>
            {validation.submit && (
              <Alert variant="danger" className="mb-3">
                {validation.submit}
              </Alert>
            )}

            <JobInfoTab
              data={formData}
              onChange={handleDataChange}
              errors={validation}
              referenceData={referenceData}
            />
          </>
        )}
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Cancel
        </Button>
        <Button 
          variant="primary" 
          onClick={handleSubmit}
          disabled={loading || referenceData.loading}
        >
          {loading ? 'Creating...' : 'Create Job'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CreateJobModal;