import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col, Spinner } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { createJob, updateJob, fetchRelatedData } from '../../store/slices/jobsSlice';

const JobModal = ({ show, handleClose, editJob = null }) => {
  const dispatch = useDispatch();
  const isEditMode = Boolean(editJob);
  
  const { 
    rigs, 
    wells, 
    operators, 
    purchaseOrders,
    loading,
    error 
  } = useSelector(state => state.jobs.relatedData);

  const initialFormState = {
    rigId: '',
    wellId: '',
    operatorId: '',
    purchaseOrderId: '',
    startDate: '',
    endDate: '',
    status: 'PENDING',
    description: '',
    estimatedDuration: '',
    actualDuration: '',
    priority: 'MEDIUM',
    notes: ''
  };

  const [formData, setFormData] = useState(initialFormState);
  const [validated, setValidated] = useState(false);

  useEffect(() => {
    if (show) {
      dispatch(fetchRelatedData());
      if (isEditMode && editJob) {
        setFormData({
          rigId: editJob.rig_id,
          wellId: editJob.well_id,
          operatorId: editJob.operator_id,
          purchaseOrderId: editJob.purchase_order_id,
          startDate: editJob.start_date,
          endDate: editJob.end_date || '',
          status: editJob.status,
          description: editJob.description,
          estimatedDuration: editJob.estimated_duration,
          actualDuration: editJob.actual_duration || '',
          priority: editJob.priority,
          notes: editJob.notes || ''
        });
      } else {
        setFormData(initialFormState);
      }
    }
  }, [show, editJob, dispatch]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    
    if (form.checkValidity() === false) {
      e.stopPropagation();
      setValidated(true);
      return;
    }

    const jobData = {
      ...formData,
      rig_id: formData.rigId,
      well_id: formData.wellId,
      operator_id: formData.operatorId,
      purchase_order_id: formData.purchaseOrderId,
      start_date: formData.startDate,
      end_date: formData.endDate,
      estimated_duration: formData.estimatedDuration,
      actual_duration: formData.actualDuration
    };

    try {
      if (isEditMode) {
        await dispatch(updateJob({ id: editJob.id, data: jobData })).unwrap();
      } else {
        await dispatch(createJob(jobData)).unwrap();
      }
      handleClose();
    } catch (err) {
      console.error('Failed to save job:', err);
    }
  };

  if (loading && !rigs.length) {
    return (
      <Modal show={show} onHide={handleClose}>
        <Modal.Body className="text-center py-4">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </Modal.Body>
      </Modal>
    );
  }

  return (
    <Modal show={show} onHide={handleClose} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{isEditMode ? 'Edit Job' : 'Create New Job'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Rig</Form.Label>
                <Form.Select 
                  name="rigId"
                  value={formData.rigId}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Rig</option>
                  {rigs.map(rig => (
                    <option key={rig.id} value={rig.id}>
                      {rig.rig_name}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  Please select a rig.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Well</Form.Label>
                <Form.Select
                  name="wellId"
                  value={formData.wellId}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Well</option>
                  {wells.map(well => (
                    <option key={well.id} value={well.id}>
                      {well.name}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  Please select a well.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Operator</Form.Label>
                <Form.Select
                  name="operatorId"
                  value={formData.operatorId}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Operator</option>
                  {operators.map(operator => (
                    <option key={operator.id} value={operator.id}>
                      {operator.name}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  Please select an operator.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Purchase Order</Form.Label>
                <Form.Select
                  name="purchaseOrderId"
                  value={formData.purchaseOrderId}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Purchase Order</option>
                  {purchaseOrders.map(po => (
                    <option key={po.id} value={po.id}>
                      {po.number}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  Please select a purchase order.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Start Date</Form.Label>
                <Form.Control
                  type="date"
                  name="startDate"
                  value={formData.startDate}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a start date.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>End Date</Form.Label>
                <Form.Control
                  type="date"
                  name="endDate"
                  value={formData.endDate}
                  onChange={handleChange}
                  min={formData.startDate}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Status</Form.Label>
                <Form.Select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  required
                >
                  <option value="PENDING">Pending</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                  <option value="CANCELLED">Cancelled</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Priority</Form.Label>
                <Form.Select
                  name="priority"
                  value={formData.priority}
                  onChange={handleChange}
                  required
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Estimated Duration (hours)</Form.Label>
                <Form.Control
                  type="number"
                  name="estimatedDuration"
                  value={formData.estimatedDuration}
                  onChange={handleChange}
                  required
                  min="0"
                />
                <Form.Control.Feedback type="invalid">
                  Please provide an estimated duration.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Actual Duration (hours)</Form.Label>
                <Form.Control
                  type="number"
                  name="actualDuration"
                  value={formData.actualDuration}
                  onChange={handleChange}
                  min="0"
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
            />
            <Form.Control.Feedback type="invalid">
              Please provide a description.
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Notes</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              name="notes"
              value={formData.notes}
              onChange={handleChange}
            />
          </Form.Group>

          <div className="d-flex justify-content-end mt-4">
            <Button variant="secondary" className="me-2" onClick={handleClose}>
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              {isEditMode ? 'Update Job' : 'Create Job'}
            </Button>
          </div>
        </Form>
      </Modal.Body>
    </Modal>
  );
};

export default JobModal;