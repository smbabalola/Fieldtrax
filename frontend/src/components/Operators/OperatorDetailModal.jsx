// File: /src/components/operators/OperatorDetailModal.jsx
import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import operatorService from '../../services/operatorService';

const OperatorDetailModal = ({ show, onHide, operator = null, onOperatorAdded, onOperatorUpdated }) => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    operator_name: '',
    company_code: '',
    address_1: '',
    address_2: '',
    post_code: '',
    zipcode: '',
    phone_no_1: '',
    phone_no_2: '',
    state: '',
    country: ''
  });

  useEffect(() => {
    if (operator) {
      setFormData({
        operator_name: operator.operator_name || '',
        company_code: operator.company_code || '',
        address_1: operator.address_1 || '',
        address_2: operator.address_2 || '',
        post_code: operator.post_code || '',
        zipcode: operator.zipcode || '',
        phone_no_1: operator.phone_no_1 || '',
        phone_no_2: operator.phone_no_2 || '',
        state: operator.state || '',
        country: operator.country || ''
      });
    } else {
      setFormData({
        operator_name: '',
        company_code: '',
        address_1: '',
        address_2: '',
        post_code: '',
        zipcode: '',
        phone_no_1: '',
        phone_no_2: '',
        state: '',
        country: ''
      });
    }
  }, [operator]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      let response;
      
      if (operator) {
        response = await operatorService.updateOperator(operator.id, formData);
        toast.success('Operator updated successfully');
        onOperatorUpdated?.(response);
      } else {
        response = await operatorService.createOperator(formData);
        toast.success('Operator added successfully');
        onOperatorAdded?.(response);
      }
      onHide();
    } catch (error) {
      console.error('Error saving operator:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{operator ? 'Edit Operator' : 'Add New Operator'}</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Operator Name <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  name="operator_name"
                  value={formData.operator_name}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Company Code</Form.Label>
                <Form.Control
                  type="text"
                  name="company_code"
                  value={formData.company_code}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Form.Group className="mb-3">
                <Form.Label>Address Line 1</Form.Label>
                <Form.Control
                  type="text"
                  name="address_1"
                  value={formData.address_1}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Form.Group className="mb-3">
                <Form.Label>Address Line 2</Form.Label>
                <Form.Control
                  type="text"
                  name="address_2"
                  value={formData.address_2}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>State</Form.Label>
                <Form.Control
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Country <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Post Code</Form.Label>
                <Form.Control
                  type="text"
                  name="post_code"
                  value={formData.post_code}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Zip Code</Form.Label>
                <Form.Control
                  type="text"
                  name="zipcode"
                  value={formData.zipcode}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Phone Number 1</Form.Label>
                <Form.Control
                  type="text"
                  name="phone_no_1"
                  value={formData.phone_no_1}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Phone Number 2</Form.Label>
                <Form.Control
                  type="text"
                  name="phone_no_2"
                  value={formData.phone_no_2}
                  onChange={handleChange}
                />
              </Form.Group>
            </Col>
          </Row>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Cancel
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? (operator ? 'Updating...' : 'Adding...') : (operator ? 'Update' : 'Add')} Operator
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default OperatorDetailModal;