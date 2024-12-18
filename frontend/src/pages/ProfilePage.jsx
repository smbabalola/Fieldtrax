// File: /frontend/src/pages/ProfilePage.jsx
import React, { useState } from 'react';
import { Card, Form, Button, Row, Col, Alert } from 'react-bootstrap';
import { useSelector, useDispatch } from 'react-redux';
import { updateUserProfile } from '../store/slices/authSlice';

const ProfilePage = () => {
  const dispatch = useDispatch();
  const { user } = useSelector(state => state.auth);
  const [isEditing, setIsEditing] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [formData, setFormData] = useState({
    email: user?.email || '',
    full_name: user?.full_name || '',
    phone: user?.phone || '',
    position: user?.position || '',
    company: user?.company || ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(updateUserProfile(formData)).unwrap();
      setShowSuccess(true);
      setIsEditing(false);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error('Failed to update profile:', error);
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
    <div className="container py-4">
      <h2 className="mb-4">Profile Settings</h2>

      {showSuccess && (
        <Alert variant="success" dismissible onClose={() => setShowSuccess(false)}>
          Profile updated successfully!
        </Alert>
      )}

      <Row>
        <Col md={8}>
          <Card className="shadow-sm">
            <Card.Header className="bg-white py-3">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0">Profile Information</h5>
                <Button
                  variant={isEditing ? "success" : "primary"}
                  onClick={() => isEditing ? handleSubmit() : setIsEditing(true)}
                >
                  {isEditing ? 'Save Changes' : 'Edit Profile'}
                </Button>
              </div>
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Full Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="full_name"
                        value={formData.full_name}
                        onChange={handleChange}
                        disabled={!isEditing}
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Email</Form.Label>
                      <Form.Control
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        disabled={!isEditing}
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Phone</Form.Label>
                      <Form.Control
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        disabled={!isEditing}
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Position</Form.Label>
                      <Form.Control
                        type="text"
                        name="position"
                        value={formData.position}
                        onChange={handleChange}
                        disabled={!isEditing}
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <Form.Group className="mb-3">
                  <Form.Label>Company</Form.Label>
                  <Form.Control
                    type="text"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    disabled={!isEditing}
                  />
                </Form.Group>
              </Form>
            </Card.Body>
          </Card>

          <Card className="shadow-sm mt-4">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0">Security Settings</h5>
            </Card.Header>
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <h6 className="mb-1">Change Password</h6>
                  <p className="text-muted mb-0">Update your password regularly to keep your account secure</p>
                </div>
                <Button variant="outline-primary">
                  Change Password
                </Button>
              </div>

              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="mb-1">Two-Factor Authentication</h6>
                  <p className="text-muted mb-0">Add an extra layer of security to your account</p>
                </div>
                <Button variant="outline-secondary">
                  Enable 2FA
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="shadow-sm">
            <Card.Header className="bg-white py-3">
              <h5 className="mb-0">Activity Log</h5>
            </Card.Header>
            <Card.Body>
              <div className="activity-timeline">
                {/* Sample activity items */}
                <div className="activity-item pb-3">
                  <div className="d-flex">
                    <div className="activity-icon me-3">
                      <i className="bi bi-person text-primary"></i>
                    </div>
                    <div>
                      <p className="mb-1">Profile updated</p>
                      <small className="text-muted">2 hours ago</small>
                    </div>
                  </div>
                </div>
                <div className="activity-item pb-3">
                  <div className="d-flex">
                    <div className="activity-icon me-3">
                      <i className="bi bi-shield-lock text-success"></i>
                    </div>
                    <div>
                      <p className="mb-1">Password changed</p>
                      <small className="text-muted">3 days ago</small>
                    </div>
                  </div>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ProfilePage;