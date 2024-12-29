// src/components/jobs/CreateJob/tabs/JobInfoTab.jsx
import React from 'react';
import { Form, Row, Col, Card, Alert } from 'react-bootstrap';

const JobInfoTab = ({ data, onChange, errors = {}, referenceData }) => {
  const JOB_STATUSES = [
    { value: 'Planned', label: 'Planned' },
    { value: 'Active', label: 'Active' },
    { value: 'In Progress', label: 'In Progress' },
    { value: 'Completed', label: 'Completed' },
    { value: 'Cancelled', label: 'Cancelled' }
  ];

  const handleFieldChange = (field, value) => {
    onChange({ [field]: value });
  };

  // Handler for operator selection
  const handleOperatorChange = (operatorId) => {
    const selectedOperator = referenceData.operators.find(op => op.id === operatorId);
    if (selectedOperator) {
      onChange({
        operator_id: operatorId,
        country: selectedOperator.country || '',
        service_code: selectedOperator.service_code || ''
      });
    } else {
      onChange({
        operator_id: operatorId,
        country: '',
        service_code: ''
      });
    }
  };

  return (
    <div>
      {referenceData.error && (
        <Alert variant="danger" className="mb-3">
          {referenceData.error}
        </Alert>
      )}

      <Card className="mb-4">
        <Card.Body>
          <h5 className="mb-3">Basic Job Information</h5>
          
          {/* Job Center and Operator Selection */}
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Center <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.jobcenter_id || ''}
                  onChange={(e) => handleFieldChange('jobcenter_id', e.target.value)}
                  isInvalid={!!errors.jobcenter_id}
                >
                  <option value="">Select Job Center</option>
                  {referenceData.jobCenters.map(center => (
                    <option key={center.id} value={center.id}>
                      {center.job_center_name}
                    </option>
                  ))}
                </Form.Select>
                {errors.jobcenter_id && (
                  <Form.Control.Feedback type="invalid">
                    {errors.jobcenter_id}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Operator <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.operator_id || ''}
                  onChange={(e) => handleOperatorChange(e.target.value)}
                  isInvalid={!!errors.operator_id}
                >
                  <option value="">Select Operator</option>
                  {referenceData.operators.map(operator => (
                    <option key={operator.id} value={operator.id}>
                      {operator.operator_name}
                    </option>
                  ))}
                </Form.Select>
                {errors.operator_id && (
                  <Form.Control.Feedback type="invalid">
                    {errors.operator_id}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
          </Row>

          {/* Job Name and Purchase Order */}
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Job Name <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  value={data.job_name || ''}
                  onChange={(e) => handleFieldChange('job_name', e.target.value)}
                  isInvalid={!!errors.job_name}
                  placeholder="Enter job name"
                />
                {errors.job_name && (
                  <Form.Control.Feedback type="invalid">
                    {errors.job_name}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Purchase Order</Form.Label>
                <Form.Select
                  value={data.purchase_order_id || ''}
                  onChange={(e) => handleFieldChange('purchase_order_id', e.target.value)}
                >
                  <option value="">Select Purchase Order</option>
                  {referenceData.purchaseOrders.map(po => (
                    <option key={po.id} value={po.id}>
                      {po.po_number}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          {/* Description */}
          <Row className="mb-4">
            <Col md={12}>
              <Form.Group>
                <Form.Label>Job Description <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={data.job_description || ''}
                  onChange={(e) => handleFieldChange('job_description', e.target.value)}
                  isInvalid={!!errors.job_description}
                  placeholder="Enter job description"
                />
                {errors.job_description && (
                  <Form.Control.Feedback type="invalid">
                    {errors.job_description}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
          </Row>

          {/* Service Code and Country */}
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Service Code</Form.Label>
                <Form.Control
                  type="text"
                  value={data.service_code || ''}
                  onChange={(e) => handleFieldChange('service_code', e.target.value)}
                  placeholder="Auto-populated from operator"
                  readOnly
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Country</Form.Label>
                <Form.Control
                  type="text"
                  value={data.country || ''}
                  onChange={(e) => handleFieldChange('country', e.target.value)}
                  placeholder="Auto-populated from operator"
                  readOnly
                />
              </Form.Group>
            </Col>
          </Row>

          <h5 className="mb-3 mt-4">Well Information</h5>
          
          {/* Well and Rig Selection */}
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Well <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.well_id || ''}
                  onChange={(e) => handleFieldChange('well_id', e.target.value)}
                  isInvalid={!!errors.well_id}
                >
                  <option value="">Select Well</option>
                  {referenceData.wells.map(well => (
                    <option key={well.id} value={well.id}>
                      {well.well_name}
                    </option>
                  ))}
                </Form.Select>
                {errors.well_id && (
                  <Form.Control.Feedback type="invalid">
                    {errors.well_id}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Rig</Form.Label>
                <Form.Select
                  value={data.rig_id || ''}
                  onChange={(e) => handleFieldChange('rig_id', e.target.value)}
                >
                  <option value="">Select Rig</option>
                  {referenceData.rigs.map(rig => (
                    <option key={rig.id} value={rig.id}>
                      {rig.rig_name}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          {/* Well Measurements */}
          <Row className="mb-4">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Measured Depth</Form.Label>
                <Form.Control
                  type="number"
                  value={data.measured_depth || ''}
                  onChange={(e) => handleFieldChange('measured_depth', Number(e.target.value))}
                  placeholder="Enter measured depth"
                  min="0"
                  step="0.01"
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Total Vertical Depth</Form.Label>
                <Form.Control
                  type="number"
                  value={data.total_vertical_depth || ''}
                  onChange={(e) => handleFieldChange('total_vertical_depth', Number(e.target.value))}
                  placeholder="Enter total vertical depth"
                  min="0"
                  step="0.01"
                />
              </Form.Group>
            </Col>
          </Row>

          <h5 className="mb-3 mt-4">Job Schedule & Status</h5>
          
          {/* Dates */}
          <Row className="mb-4">
            <Col md={4}>
              <Form.Group>
                <Form.Label>Spud Date</Form.Label>
                <Form.Control
                  type="datetime-local"
                  value={data.spud_date || ''}
                  onChange={(e) => handleFieldChange('spud_date', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Mobilization Date</Form.Label>
                <Form.Control
                  type="datetime-local"
                  value={data.mobilization_date || ''}
                  onChange={(e) => handleFieldChange('mobilization_date', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Demobilization Date</Form.Label>
                <Form.Control
                  type="datetime-local"
                  value={data.demobilization_date || ''}
                  onChange={(e) => handleFieldChange('demobilization_date', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          {/* Status and Options */}
          <Row className="mb-4">
            <Col md={12}>
              <Form.Group>
                <Form.Label>Status <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.status || 'Planned'}
                  onChange={(e) => handleFieldChange('status', e.target.value)}
                  isInvalid={!!errors.status}
                >
                  {JOB_STATUSES.map(status => (
                    <option key={status.value} value={status.value}>
                      {status.label}
                    </option>
                  ))}
                </Form.Select>
                {errors.status && (
                  <Form.Control.Feedback type="invalid">
                    {errors.status}
                  </Form.Control.Feedback>
                )}
              </Form.Group>
            </Col>
          </Row>

          {/* Additional Options */}
          <Row>
            <Col md={6}>
              <Form.Group>
                <Form.Check
                  type="checkbox"
                  id="job_closed"
                  label="Job Closed"
                  checked={data.job_closed || false}
                  onChange={(e) => handleFieldChange('job_closed', e.target.checked)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group>
                <Form.Check
                  type="checkbox"
                  id="trainingfile"
                  label="Training File"
                  checked={data.trainingfile || false}
                  onChange={(e) => handleFieldChange('trainingfile', e.target.checked)}
                />
              </Form.Group>
            </Col>
          </Row>

        </Card.Body>
      </Card>
    </div>
  );
};

export default JobInfoTab;