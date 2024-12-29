// File: /src/components/wells/WellDetailModal.jsx
import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import wellService from '../../services/wellService';

const WellDetailModal = ({ show, onHide, operatorId, well = null, onWellAdded, onWellUpdated }) => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    well_name: '',
    api_number: '',
    field_name: '',
    location: '',
    county: '',
    state: '',
    country: '',
    operator_id: operatorId
  });

  useEffect(() => {
    if (well) {
      setFormData({
        well_name: well.well_name || '',
        api_number: well.api_number || '',
        field_name: well.field_name || '',
        location: well.location || '',
        county: well.county || '',
        state: well.state || '',
        country: well.country || '',
        operator_id: operatorId
      });
    } else {
      setFormData({
        well_name: '',
        api_number: '',
        field_name: '',
        location: '',
        county: '',
        state: '',
        country: '',
        operator_id: operatorId
      });
    }
  }, [well, operatorId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await wellService.createWell(formData);
      toast.success('Well added successfully');
      onWellAdded(response);
      onHide();
    } catch (error) {
      console.error('Error saving well:', error);
      toast.error('Failed to save well');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{well ? 'Edit Well' : 'Add New Well'}</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Well Name <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  name="well_name"
                  value={formData.well_name}
                  onChange={(e) => setFormData({ ...formData, well_name: e.target.value })}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>API Number</Form.Label>
                <Form.Control
                  type="text"
                  name="api_number"
                  value={formData.api_number}
                  onChange={(e) => setFormData({ ...formData, api_number: e.target.value })}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Field Name</Form.Label>
                <Form.Control
                  type="text"
                  name="field_name"
                  value={formData.field_name}
                  onChange={(e) => setFormData({ ...formData, field_name: e.target.value })}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Location</Form.Label>
                <Form.Control
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>County</Form.Label>
                <Form.Control
                  type="text"
                  name="county"
                  value={formData.county}
                  onChange={(e) => setFormData({ ...formData, county: e.target.value })}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>State</Form.Label>
                <Form.Control
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Country</Form.Label>
                <Form.Control
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={(e) => setFormData({ ...formData, country: e.target.value })}
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
            {loading ? 'Saving...' : 'Save Well'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default WellDetailModal;