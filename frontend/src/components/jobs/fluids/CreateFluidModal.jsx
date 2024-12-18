// File: /frontend/src/components/jobs/fluids/CreateFluidModal.jsx
import React, { useState } from 'react';
import { Modal, Form, Button, Row, Col } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { createFluid } from '../../../store/slices/fluidsSlice';

const CreateFluidModal = ({ show, onHide }) => {
  const dispatch = useDispatch();
  const { loading } = useSelector(state => state.fluids);
  
  const [formData, setFormData] = useState({
    type: '',
    volume: '',
    density: '',
    viscosity: '',
    description: '',
    ph: '',
    chlorides: '',
    additives: [],
    status: 'ACTIVE'
  });

  const [validated, setValidated] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    
    if (form.checkValidity() === false) {
      event.stopPropagation();
      setValidated(true);
      return;
    }

    try {
      await dispatch(createFluid(formData)).unwrap();
      onHide();
      setFormData({});
    } catch (error) {
      console.error('Failed to create fluid:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value
    }));
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Add New Fluid</Modal.Title>
        </Modal.Header>
        
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Fluid Type*</Form.Label>
                <Form.Select
                  required
                  name="type"
                  value={formData.type}
                  onChange={handleChange}
                >
                  <option value="">Select Type</option>
                  <option value="DRILLING">Drilling Fluid</option>
                  <option value="COMPLETION">Completion Fluid</option>
                  <option value="WORKOVER">Workover Fluid</option>
                  <option value="SPACER">Spacer</option>
                  <option value="PILLS">Pills</option>
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  Please select a fluid type.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Volume (bbl)*</Form.Label>
                <Form.Control
                  required
                  type="number"
                  step="0.01"
                  name="volume"
                  value={formData.volume}
                  onChange={handleChange}
                  placeholder="Enter volume"
                />
                <Form.Control.Feedback type="invalid">
                  Please enter a valid volume.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Density (ppg)*</Form.Label>
                <Form.Control
                  required
                  type="number"
                  step="0.1"
                  name="density"
                  value={formData.density}
                  onChange={handleChange}
                  placeholder="Enter density"
                />
                <Form.Control.Feedback type="invalid">
                  Please enter a valid density.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Viscosity (cp)*</Form.Label>
                <Form.Control
                  required
                  type="number"
                  step="0.1"
                  name="viscosity"
                  value={formData.viscosity}
                  onChange={handleChange}
                  placeholder="Enter viscosity"
                />
                <Form.Control.Feedback type="invalid">
                  Please enter a valid viscosity.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>pH</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  name="ph"
                  value={formData.ph}
                  onChange={handleChange}
                  placeholder="Enter pH"
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3">
            <Form.Label>Chlorides (ppm)</Form.Label>
            <Form.Control
              type="number"
              name="chlorides"
              value={formData.chlorides}
              onChange={handleChange}
              placeholder="Enter chlorides content"
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter fluid description"
            />
          </Form.Group>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading}>
            {loading ? 'Adding...' : 'Add Fluid'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default CreateFluidModal;