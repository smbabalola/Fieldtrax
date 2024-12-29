// src/components/jobs/JobDetailModal.jsx
import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import CustomerInfoTab from './CreateJob/tabs/CustomerInfoTab';

const JobDetailModal = ({ show, onHide, onSubmit }) => {
  const [formData, setFormData] = useState({
    job_name: '',
    job_center_id: '',
    job_description: '',
    operator_id: '',
    operator_name: '',
    service_code: '',
    country: '',
    purchase_order_id: ''
  });
  
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    if (!formData.job_name) newErrors.job_name = 'Job name is required';
    if (!formData.job_center_id) newErrors.job_center_id = 'Job center is required';
    if (!formData.job_description) newErrors.job_description = 'Job description is required';
    if (!formData.operator_id) newErrors.operator_id = 'Operator is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (updatedData) => {
    setFormData(prev => ({
      ...prev,
      ...updatedData
    }));
    
    // Clear validation errors for updated fields
    const updatedFields = Object.keys(updatedData);
    if (updatedFields.length > 0) {
      setErrors(prev => {
        const newErrors = { ...prev };
        updatedFields.forEach(field => {
          delete newErrors[field];
        });
        return newErrors;
      });
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="xl" backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title>Create New Job</Modal.Title>
      </Modal.Header>
      
      <Modal.Body>
        <CustomerInfoTab 
          data={formData}
          onChange={handleChange}
          errors={errors}
        />
      </Modal.Body>
      
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cancel
        </Button>
        <Button 
          variant="primary" 
          onClick={handleSubmit}
        >
          Create Job
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default JobDetailModal;
