

// File: src/pages/ForgotPasswordPage.jsx
import React, { useState } from 'react';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await axios.post(`${API_URL}/users/auth/forgot-password`, {
        email
      });

      setSuccess(true);
    } catch (err) {
      console.error('Password reset request error:', err);
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        'Failed to process password reset request'
      );
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <Container fluid className="vh-100 d-flex align-items-center justify-content-center bg-light">
        <div className="text-center p-4 bg-white rounded shadow" style={{ width: '100%', maxWidth: '400px' }}>
          <h4 className="mb-4">Reset Link Sent</h4>
          <p className="text-muted">
            If an account exists with the email {email}, you will receive a password reset link shortly.
          </p>
          <p className="mb-4">Please check your email and follow the instructions.</p>
          <Link to="/login" className="btn btn-primary">
            Return to Login
          </Link>
        </div>
      </Container>
    );
  }

  return (
    <Container fluid className="vh-100 d-flex align-items-center justify-content-center bg-light">
      <div className="p-4 bg-white rounded shadow" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 className="text-center mb-4">Reset Password</h2>
        
        {error && (
          <Alert variant="danger" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        )}
        
        <p className="text-muted mb-4">
          Enter your email address and we'll send you a link to reset your password.
        </p>

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-4">
            <Form.Label>Email Address</Form.Label>
            <Form.Control
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
              placeholder="Enter your email"
              autoComplete="email"
            />
          </Form.Group>

          <div className="d-grid gap-2">
            <Button 
              variant="primary" 
              type="submit" 
              disabled={loading}
              size="lg"
            >
              {loading ? (
                <>
                  <span 
                    className="spinner-border spinner-border-sm me-2" 
                    role="status" 
                    aria-hidden="true"
                  />
                  Sending Reset Link...
                </>
              ) : (
                'Send Reset Link'
              )}
            </Button>

            <Link 
              to="/login" 
              className="btn btn-link"
            >
              Back to Login
            </Link>
          </div>
        </Form>
      </div>
    </Container>
  );
};

export default ForgotPasswordPage;