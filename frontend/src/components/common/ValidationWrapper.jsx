// src/components/common/ValidationWrapper.jsx
import React from 'react';
import { Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

const ValidationWrapper = ({ 
  children, 
  error, 
  touched, 
  label, 
  required = false,
  helpText,
  className = ''
}) => {
  const showError = error && touched;
  
  return (
    <Form.Group className={`mb-3 ${className}`}>
      {label && (
        <Form.Label>
          {label}
          {required && <span className="text-danger ms-1">*</span>}
        </Form.Label>
      )}
      
      {children}
      
      {showError && (
        <Form.Control.Feedback type="invalid" className="d-block">
          {error}
        </Form.Control.Feedback>
      )}
      
      {helpText && !showError && (
        <Form.Text className="text-muted">
          {helpText}
        </Form.Text>
      )}
    </Form.Group>
  );
};

ValidationWrapper.propTypes = {
  children: PropTypes.node.isRequired,
  error: PropTypes.string,
  touched: PropTypes.bool,
  label: PropTypes.string,
  required: PropTypes.bool,
  helpText: PropTypes.string,
  className: PropTypes.string
};

export default ValidationWrapper;