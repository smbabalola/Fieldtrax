// File: /frontend/src/pages/job/tabs/JobInfoTab.jsx
import React, { useState, useEffect } from 'react';
import { Form, Row, Col, Button, Card, Badge, Spinner } from 'react-bootstrap';
import { toast } from 'react-toastify';
import './JobInfoTab.css'; // We'll create this CSS file separately

const ActivityList = ({ activities, loading }) => {
  const getActivityTypeColor = (type) => {
    const colors = {
      mobilization: 'primary',
      demobilization: 'secondary',
      equipment_delivery: 'info',
      start_job: 'success',
      end_job: 'warning',
      incident: 'danger',
      NPT: 'dark'
    };
    return colors[type] || 'secondary';
  };

  if (loading) {
    return (
      <div className="text-center p-4">
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  return (
    <div className="activity-list">
      <h5 className="mb-3">Activity History</h5>
      <div className="timeline">
        {activities && activities.length > 0 ? (
          activities.map((activity, index) => (
            <Card key={activity.id || index} className="mb-3 border-0 shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <Badge bg={getActivityTypeColor(activity.type)} className="mb-2">
                      {activity.type.replace('_', ' ').toUpperCase()}
                    </Badge>
                    <p className="mb-1">{activity.description}</p>
                    <small className="text-muted">
                      By {activity.user?.name || 'Unknown User'} • 
                      {new Date(activity.timestamp).toLocaleString()}
                    </small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          ))
        ) : (
          <Card className="border-0 shadow-sm">
            <Card.Body className="text-center text-muted">
              <p className="mb-0">No activities recorded yet</p>
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

const JobInfoTab = ({ job, onSave }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    jobName: job?.jobName || '',
    jobNumber: job?.jobNumber || '',
    operator: job?.operator || '',
    wellName: job?.wellName || '',
    field: job?.field || '',
    country: job?.country || '',
    status: job?.status || 'planned',
    startDate: job?.startDate || '',
    endDate: job?.endDate || '',
    description: job?.description || ''
  });
  
  const [activities, setActivities] = useState([]);
  const [loadingActivities, setLoadingActivities] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        setLoadingActivities(true);
        // Mock data for testing
        const mockActivities = [
          {
            id: '1',
            type: 'mobilization',
            description: 'Initial job planning meeting completed',
            timestamp: '2024-03-18T09:00:00Z',
            user: { name: 'John Doe' }
          },
          {
            id: '2',
            type: 'equipment_delivery',
            description: 'Primary tools package arrived at staging area',
            timestamp: '2024-03-19T14:00:00Z',
            user: { name: 'Jane Smith' }
          },
          {
            id: '3',
            type: 'start_job',
            description: 'Pre-job safety meeting conducted',
            timestamp: '2024-03-20T06:00:00Z',
            user: { name: 'John Doe' }
          }
        ];
        setActivities(mockActivities);
      } catch (error) {
        toast.error('Failed to load activities');
        console.error('Error loading activities:', error);
      } finally {
        setLoadingActivities(false);
      }
    };

    if (job?.id) {
      fetchActivities();
    }
  }, [job?.id]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await onSave(formData);
      setIsEditing(false);
      toast.success('Job information updated successfully');
    } catch (error) {
      toast.error('Failed to update job information');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="job-info-tab">
      {/* Job Information Form */}
      <div className="mb-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h5 className="mb-0">Job Information</h5>
          {!isEditing && (
            <Button
              variant="primary"
              size="sm"
              onClick={() => setIsEditing(true)}
              disabled={saving}
            >
              <i className="bi bi-pencil me-2"></i>
              Edit
            </Button>
          )}
        </div>

        <Form onSubmit={handleSubmit}>
          <Row className="g-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Name</Form.Label>
                <Form.Control
                  type="text"
                  name="jobName"
                  value={formData.jobName}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Number</Form.Label>
                <Form.Control
                  type="text"
                  name="jobNumber"
                  value={formData.jobNumber}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Operator</Form.Label>
                <Form.Control
                  type="text"
                  name="operator"
                  value={formData.operator}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Well Name</Form.Label>
                <Form.Control
                  type="text"
                  name="wellName"
                  value={formData.wellName}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Field</Form.Label>
                <Form.Control
                  type="text"
                  name="field"
                  value={formData.field}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Country</Form.Label>
                <Form.Control
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Status</Form.Label>
                <Form.Select
                  name="status"
                  value={formData.status}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                  required
                >
                  <option value="planned">Planned</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </Form.Select>
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Start Date</Form.Label>
                <Form.Control
                  type="date"
                  name="startDate"
                  value={formData.startDate}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                />
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>End Date</Form.Label>
                <Form.Control
                  type="date"
                  name="endDate"
                  value={formData.endDate}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                />
              </Form.Group>
            </Col>

            <Col md={12}>
              <Form.Group>
                <Form.Label>Description</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  disabled={!isEditing || saving}
                />
              </Form.Group>
            </Col>

            {isEditing && (
              <Col xs={12}>
                <div className="d-flex justify-content-end gap-2">
                  <Button 
                    variant="outline-secondary" 
                    onClick={() => {
                      setFormData({
                        jobName: job?.jobName || '',
                        jobNumber: job?.jobNumber || '',
                        operator: job?.operator || '',
                        wellName: job?.wellName || '',
                        field: job?.field || '',
                        country: job?.country || '',
                        status: job?.status || 'planned',
                        startDate: job?.startDate || '',
                        endDate: job?.endDate || '',
                        description: job?.description || ''
                      });
                      setIsEditing(false);
                    }}
                    disabled={saving}
                  >
                    Cancel
                  </Button>
                  <Button 
                    type="submit" 
                    variant="primary"
                    disabled={saving}
                  >
                    {saving ? (
                      <>
                        <Spinner
                          as="span"
                          animation="border"
                          size="sm"
                          role="status"
                          aria-hidden="true"
                          className="me-2"
                        />
                        Saving...
                      </>
                    ) : (
                      'Save Changes'
                    )}
                  </Button>
                </div>
              </Col>
            )}
          </Row>
        </Form>
      </div>

      {/* Activity List */}
      <Card className="mt-4">
        <Card.Body>
          <ActivityList 
            activities={activities}
            loading={loadingActivities}
          />
        </Card.Body>
      </Card>
    </div>
  );
};

export default JobInfoTab;