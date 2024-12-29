// src/components/jobs/CreateJob/tabs/CustomerInfoTab.jsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { Form, Row, Col, Card, Button, Alert } from 'react-bootstrap';
import operatorService from '../../../../services/operatorService';
import purchaseOrderService from '../../../../services/purchaseOrderService';
import OperatorDetailModal from '../../../operators/OperatorDetailModal';
import PurchaseOrderModal from '../../../purchaseOrders/PurchaseOrderModal';
import jobCenterService from '../../../../services/jobCenterService';

const CustomerInfoTab = ({ data, onChange, errors = {}, isUpdateMode = false }) => {
  // State Management
  const [loading, setLoading] = useState(false);
  const [operators, setOperators] = useState([]);
  const [jobCenters, setJobCenters] = useState([]);
  const [purchaseOrders, setPurchaseOrders] = useState([]);
  const [showOperatorModal, setShowOperatorModal] = useState(false);
  const [showPOModal, setShowPOModal] = useState(false);
  const [error, setError] = useState(null);
  const [jobCentersLoading, setJobCentersLoading] = useState(false);

  // Unified update handler
  const handleDataUpdate = (updates) => {
    if (!onChange) {
      console.warn('onChange function not provided to CustomerInfoTab');
      return;
    }

    try {
      const updatedData = {
        ...data,
        ...updates
      };
      onChange(updatedData);
    } catch (err) {
      console.error('Error updating data:', err);
      setError('Failed to update form data');
      toast.error('Failed to update form data');
    }
  };

  // Fetch Job Centers
  useEffect(() => {
    const fetchJobCenters = async () => {
      try {
        setJobCentersLoading(true);
        setError(null);
        const response = await jobCenterService.getAll();
        if (response?.data) {
          setJobCenters(response.data);
        } else if (Array.isArray(response)) {
          setJobCenters(response);
        }
      } catch (err) {
        console.error('Error fetching job centers:', err);
        setError('Failed to load job centers');
      } finally {
        setJobCentersLoading(false);
      }
    };

    fetchJobCenters();
  }, []);

  // Fetch Operators
  useEffect(() => {
    const fetchOperators = async () => {
      try {
        setLoading(true);
        const response = await operatorService.getAll();
        if (response?.items) {
          setOperators(response.items);
        } else if (Array.isArray(response)) {
          setOperators(response);
        }
      } catch (err) {
        console.error('Error fetching operators:', err);
        setError('Failed to load operators');
      } finally {
        setLoading(false);
      }
    };

    fetchOperators();
  }, []);

  // Fetch Purchase Orders when operator changes
  useEffect(() => {
    const fetchPurchaseOrders = async () => {
      if (data.operator_id) {
        try {
          const response = await purchaseOrderService.getPurchaseOrders({ 
            operator_id: data.operator_id 
          });
          if (response?.data) {
            setPurchaseOrders(response.data);
          } else if (Array.isArray(response)) {
            setPurchaseOrders(response);
          }
        } catch (err) {
          console.error('Error fetching purchase orders:', err);
          toast.error('Failed to load purchase orders');
        }
      }
    };

    fetchPurchaseOrders();
  }, [data.operator_id]);

  const handleOperatorChange = (e) => {
    const selectedOperatorId = e.target.value;
    const selectedOperator = operators.find(op => op.id === selectedOperatorId);
    
    if (selectedOperator) {
      handleDataUpdate({
        operator_id: selectedOperator.id,
        operator_name: selectedOperator.operator_name,
        country: selectedOperator.country || '',
        service_code: selectedOperator.service_code || ''
      });
      
      // Reset purchase order when operator changes
      handleDataUpdate({ purchase_order_id: '' });
    }
  };

  const handleOperatorAdded = (newOperator) => {
    setOperators(prev => [...prev, newOperator]);
    
    // Automatically select the newly added operator
    handleDataUpdate({
      operator_id: newOperator.id,
      operator_name: newOperator.operator_name,
      country: newOperator.country || '',
      service_code: newOperator.service_code || ''
    });
    
    setShowOperatorModal(false);
    toast.success('Operator added successfully');
  };

  const handlePurchaseOrderCreated = async (newPO) => {
    try {
      handleDataUpdate({
        purchase_order_id: newPO.id,
        po_number: newPO.po_number,
        well_id: newPO.well_id || data.well_id
      });

      // Refresh PO list
      const response = await purchaseOrderService.getPurchaseOrders({ 
        operator_id: data.operator_id 
      });
      
      if (response?.data) {
        setPurchaseOrders(response.data);
      } else if (Array.isArray(response)) {
        setPurchaseOrders(response);
      }

      setShowPOModal(false);
      toast.success('Purchase order created successfully');
    } catch (err) {
      console.error('Error handling new purchase order:', err);
      toast.error('Failed to update purchase order information');
    }
  };

  const handleFieldChange = (field, value) => {
    handleDataUpdate({ [field]: value });
  };

  return (
    <div>
      {error && (
        <Alert variant="danger" onClose={() => setError(null)} dismissible>
          {error}
        </Alert>
      )}

      <Card className="mb-4">
        <Card.Body>
          {/* Job Details Section */}
          <h5 className="mb-3">Job Details</h5>
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Name <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  value={data.job_name || ''}
                  onChange={(e) => handleFieldChange('job_name', e.target.value)}
                  placeholder="Enter job name"
                  isInvalid={!!errors.job_name}
                />
                {errors.job_name && (
                  <Form.Control.Feedback type="invalid">
                    {errors.job_name}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Center <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.job_center_id || ''}
                  onChange={(e) => handleFieldChange('job_center_id', e.target.value)}
                  isInvalid={!!errors.job_center_id}
                  disabled={jobCentersLoading}
                >
                  <option value="">Select Job Center</option>
                  {jobCenters.map(center => (
                    <option key={center.id} value={center.id}>
                      {center.job_center_name}
                    </option>
                  ))}
                </Form.Select>
                {errors.job_center_id && (
                  <Form.Control.Feedback type="invalid">
                    {errors.job_center_id}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
          </Row>

          <Row className="mb-4">
            <Col md={12}>
              <Form.Group>
                <Form.Label>Job Description <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={data.job_description || ''}
                  onChange={(e) => handleFieldChange('job_description', e.target.value)}
                  placeholder="Enter job description"
                  isInvalid={!!errors.job_description}
                />
                {errors.job_description && (
                  <Form.Control.Feedback type="invalid">
                    {errors.job_description}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
          </Row>

          {/* Customer Information Section */}
          <h5 className="mb-3">Customer Information</h5>
          <Row>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Operator <span className="text-danger">*</span></Form.Label>
                <div className="d-flex gap-2">
                  <Form.Select
                    value={data.operator_id || ''}
                    onChange={handleOperatorChange}
                    isInvalid={!!errors.operator_id}
                    disabled={loading}
                  >
                    <option value="">Select Operator</option>
                    {operators.map(operator => (
                      <option key={operator.id} value={operator.id}>
                        {operator.operator_name}
                      </option>
                    ))}
                  </Form.Select>
                  <Button 
                    variant="outline-primary"
                    onClick={() => setShowOperatorModal(true)}
                  >
                    Add New
                  </Button>
                </div>
                {errors.operator_id && (
                  <Form.Control.Feedback type="invalid">
                    {errors.operator_id}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Service Code</Form.Label>
                <Form.Control
                  type="text"
                  value={data.service_code || ''}
                  onChange={(e) => handleFieldChange('service_code', e.target.value)}
                  placeholder="Service code will be populated from operator"
                  readOnly
                />
              </Form.Group>
            </Col>
          </Row>

          <Row className="mt-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Country</Form.Label>
                <Form.Control
                  type="text"
                  value={data.country || ''}
                  onChange={(e) => handleFieldChange('country', e.target.value)}
                  placeholder="Country will be populated from operator"
                  readOnly
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Purchase Order</Form.Label>
                <div className="d-flex gap-2">
                  <Form.Select
                    value={data.purchase_order_id || ''}
                    onChange={(e) => handleFieldChange('purchase_order_id', e.target.value)}
                  >
                    <option value="">Select Purchase Order</option>
                    {purchaseOrders.map(po => (
                      <option key={po.id} value={po.id}>
                        {po.po_number} - {po.supplier_name}
                      </option>
                    ))}
                  </Form.Select>
                  <Button
                    variant="outline-primary"
                    onClick={() => setShowPOModal(true)}
                    disabled={!data.operator_id}
                  >
                    {!data.operator_id ? 'Select Operator First' : 'New PO'}
                  </Button>
                </div>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Modals */}
      <OperatorDetailModal 
        show={showOperatorModal}
        onHide={() => setShowOperatorModal(false)}
        onOperatorAdded={handleOperatorAdded}
      />

      <PurchaseOrderModal
        show={showPOModal}
        onHide={() => setShowPOModal(false)}
        onSuccess={handlePurchaseOrderCreated}
        wellId={data.well_id}
        operatorId={data.operator_id}
      />
    </div>
  );
};

export default CustomerInfoTab;