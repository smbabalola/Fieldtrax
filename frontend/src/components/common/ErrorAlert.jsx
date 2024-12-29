// ErrorAlert.jsx
import React from 'react';
import { Alert } from 'react-bootstrap';

const ErrorAlert = ({ error, onClose }) => {
  if (!error) {
    return null; // Don't render if there's no error
  }

  return (
    <Alert variant="danger" onClose={onClose} dismissible>
      {error}
    </Alert>
  );
};

export default ErrorAlert;