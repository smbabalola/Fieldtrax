// src/components/jobs/CreateJobModal.jsx
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Modal, Form, Button, Row, Col, Alert, Spinner } from 'react-bootstrap';
import { createJob } from '../../store/slices/jobsSlice';
import { selectCreateJobModal, closeCreateJobModal } from '../../store/slices/uiSlice';
import wellService from '../../services/wellService';
import operatorService from '../../services/operatorService';
import rigService from '../../services/rigService';
import purchaseOrderService from '../../services/purchaseOrderService';
import jobCenterService from '../../services/jobCenterService';

const initialFormData = {
  jobcenter_id: '',
  job_name: '',
  job_description: '',
  rig_id: '',
  purchase_order_id: '',
  operator_id: '',
  well_id: '',
  service_code: '',
  country: '',
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

      // Ensure we handle both array responses and paginated responses with items property
      const extractItems = (response) => {
        if (!response) return [];
        if (Array.isArray(response)) return response;
        if (response.items && Array.isArray(response.items)) return response.items;
        if (response.data && Array.isArray(response.data)) return response.data;
        console.warn('Unexpected response format:', response);
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
        wells: [],
        operators: [],
        rigs: [],
        purchaseOrders: [],
        jobCenters: [],
        loading: false,
        error: 'Failed to load reference data. Please try again.'
      }));
    }
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.job_name) errors.job_name = 'Job name is required';
    if (!formData.jobcenter_id) errors.jobcenter_id = 'Job center is required';
    if (!formData.well_id) errors.well_id = 'Well is required';
    if (!formData.operator_id) errors.operator_id = 'Operator is required';
    
    setValidation(errors);
    return Object.keys(errors).length === 0;
  };

  const handleClose = () => {
    dispatch(closeCreateJobModal());
    setFormData(initialFormData);
    setValidation({});
  };

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let newValue = type === 'checkbox' ? e.target.checked : value;
    
    // Handle numeric fields
    if (type === 'number') {
      newValue = value === '' ? '' : Number(value);
    }

    setFormData(prev => ({
      ...prev,
      [name]: newValue
    }));
    
    // Clear validation error when field is changed
    if (validation[name]) {
      setValidation(prev => ({ ...prev, [name]: '' }));
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
    <Modal show={isOpen} onHide={handleClose} size="lg">
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
          <Form onSubmit={handleSubmit}>
            {validation.submit && (
              <Alert variant="danger" className="mb-3">
                {validation.submit}
              </Alert>
            )}

            <Row className="mb-3">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Job Center *</Form.Label>
                  <Form.Select
                    name="jobcenter_id"
                    value={formData.jobcenter_id}
                    onChange={handleChange}
                    isInvalid={!!validation.jobcenter_id}
                  >
                    <option value="">Select Job Center</option>
                    {referenceData.jobCenters.map(center => (
                      <option key={center.id} value={center.id}>
                        {center.job_center_name}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Control.Feedback type="invalid">
                    {validation.jobcenter_id}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Job Name *</Form.Label>
                  <Form.Control
                    type="text"
                    name="job_name"
                    value={formData.job_name}
                    onChange={handleChange}
                    isInvalid={!!validation.job_name}
                  />
                  <Form.Control.Feedback type="invalid">
                    {validation.job_name}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
            </Row>

            {/* Additional rows... */}

            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="job_description"
                value={formData.job_description}
                onChange={handleChange}
              />
            </Form.Group>

            <Row className="mb-3">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Well *</Form.Label>
                  <Form.Select
                    name="well_id"
                    value={formData.well_id}
                    onChange={handleChange}
                    isInvalid={!!validation.well_id}
                  >
                    <option value="">Select Well</option>
                    {referenceData.wells.map(well => (
                      <option key={well.id} value={well.id}>
                        {well.well_name}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Control.Feedback type="invalid">
                    {validation.well_id}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Operator *</Form.Label>
                  <Form.Select
                    name="operator_id"
                    value={formData.operator_id}
                    onChange={handleChange}
                    isInvalid={!!validation.operator_id}
                  >
                    <option value="">Select Operator</option>
                    {referenceData.operators.map(operator => (
                      <option key={operator.id} value={operator.id}>
                        {operator.operator_name}
                      </option>
                    ))}
                  </Form.Select>
                  <Form.Control.Feedback type="invalid">
                    {validation.operator_id}
                  </Form.Control.Feedback>
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Rig</Form.Label>
                  <Form.Select
                    name="rig_id"
                    value={formData.rig_id}
                    onChange={handleChange}
                  >
                    <option value="">Select Rig</option>
                    {referenceData.rigs.map(rig => (
                      <option key={rig.id} value={rig.id}>
                        {rig.rig_name}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Purchase Order</Form.Label>
                  <Form.Select
                    name="purchase_order_id"
                    value={formData.purchase_order_id}
                    onChange={handleChange}
                  >
                    <option value="">Select Purchase Order</option>
                    {referenceData.purchaseOrders.map(po => (
                      <option key={po.id} value={po.id}>
                        {po.po_number}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            {/* ... rest of the form fields ... */}
          </Form>
        )}
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Cancel </Button>
        <Button 
          variant="primary" 
          onClick={handleSubmit}
          disabled={loading || referenceData.loading}
        >
          {loading ? 'Creating...' : 'Create Job'}
        </Button>
      </Modal.Footer>

      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Service Code</Form.Label>
            <Form.Control
              type="text"
              name="service_code"
              value={formData.service_code}
              onChange={handleChange}
              placeholder="Enter service code"
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group>
            <Form.Label>Country</Form.Label>
            <Form.Control
              type="text"
              name="country"
              value={formData.country}
              onChange={handleChange}
              placeholder="Enter country"
            />
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Measured Depth</Form.Label>
            <Form.Control
              type="number"
              name="measured_depth"
              value={formData.measured_depth}
              onChange={handleChange}
              min="0"
              step="0.01"
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group>
            <Form.Label>Total Vertical Depth</Form.Label>
            <Form.Control
              type="number"
              name="total_vertical_depth"
              value={formData.total_vertical_depth}
              onChange={handleChange}
              min="0"
              step="0.01"
            />
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Spud Date</Form.Label>
            <Form.Control
              type="datetime-local"
              name="spud_date"
              value={formData.spud_date}
              onChange={handleChange}
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group>
            <Form.Label>Status</Form.Label>
            <Form.Select
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="Planned">Planned</option>
              <option value="Active">Active</option>
              <option value="In Progress">In Progress</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Label>Mobilization Date</Form.Label>
            <Form.Control
              type="datetime-local"
              name="mobilization_date"
              value={formData.mobilization_date}
              onChange={handleChange}
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group>
            <Form.Label>Demobilization Date</Form.Label>
            <Form.Control
              type="datetime-local"
              name="demobilization_date"
              value={formData.demobilization_date}
              onChange={handleChange}
            />
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Check
              type="checkbox"
              id="job_closed"
              name="job_closed"
              label="Job Closed"
              checked={formData.job_closed}
              onChange={handleChange}
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group>
            <Form.Check
              type="checkbox"
              id="trainingfile"
              name="trainingfile"
              label="Training File"
              checked={formData.trainingfile}
              onChange={handleChange}
            />
          </Form.Group>
        </Col>
      </Row>
    </Modal>
  );
};

export default CreateJobModal;