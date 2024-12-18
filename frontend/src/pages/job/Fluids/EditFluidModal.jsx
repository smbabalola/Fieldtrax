// File: /frontend/src/pages/jobs/Fluids/EditFluidModal.jsx
import React, { useState } from 'react';
import { Modal, Form, Button } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import { updateFluid } from '../../../store/slices/fluidsSlice';

const EditFluidModal = ({ show, onHide, fluid, jobId }) => {
  const dispatch = useDispatch();
  const [validated, setValidated] = useState(false);
  const [formData, setFormData] = useState({
    type: fluid.type,
    volume: fluid.volume,
    density: fluid.density,
    viscosity: fluid.viscosity
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    
    if (form.checkValidity() === false) {
      e.stopPropagation();
      setValidated(true);
      return;
    }

    try {
      await dispatch(updateFluid({ 
        id: fluid.id,
        ...formData,
        jobId 
      })).unwrap();
      onHide();
    } catch (error) {
      console.error('Failed to update fluid:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Fluid</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Fluid Type</Form.Label>
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

          <Form.Group className="mb-3">
            <Form.Label>Volume (bbl)</Form.Label>
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

          <Form.Group className="mb-3">
            <Form.Label>Density (ppg)</Form.Label>
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

          <Form.Group className="mb-3">
            <Form.Label>Viscosity (cp)</Form.Label>
            <Form.Control
              type="number"
              step="0.1"
              name="viscosity"
              value={formData.viscosity}
              onChange={handleChange}
              placeholder="Enter viscosity"
            />
          </Form.Group>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Cancel
          </Button>
          <Button type="submit">
            Save Changes
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EditFluidModal;