// File: /src/components/jobs/CreateJob/modals/CasingModal.jsx
import React from 'react';
import { Modal, Form, Row, Col, Button } from 'react-bootstrap';
import { standardGrades, standardThreads } from '../../../../utils/tubularStandards';

const CasingModal = ({
  show,
  onHide,
  casing,
  onChange,
  onSubmit,
  isEditing
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{isEditing ? 'Edit Casing' : 'Add Casing'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Outer Diameter (in) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.001"
                  value={casing.outer_diameter || ''}
                  onChange={(e) => onChange('outer_diameter', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Inner Diameter (in) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.001"
                  value={casing.inner_diameter || ''}
                  onChange={(e) => onChange('inner_diameter', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Weight (lbs/ft) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.01"
                  value={casing.weight || ''}
                  onChange={(e) => onChange('weight', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Grade <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={casing.grade || ''}
                  onChange={(e) => onChange('grade', e.target.value)}
                  required
                >
                  <option value="">Select Grade</option>
                  {standardGrades.map(grade => (
                    <option key={grade} value={grade}>{grade}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Thread Type <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={casing.thread || ''}
                  onChange={(e) => onChange('thread', e.target.value)}
                  required
                >
                  <option value="">Select Thread Type</option>
                  {standardThreads.map(thread => (
                    <option key={thread} value={thread}>{thread}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Open Hole Size (in)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.001"
                  value={casing.open_hole_size || ''}
                  onChange={(e) => onChange('open_hole_size', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Start Depth (ft) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={casing.start_depth || ''}
                  onChange={(e) => onChange('start_depth', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>End Depth (ft) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={casing.end_depth || ''}
                  onChange={(e) => onChange('end_depth', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Cement Top (ft)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={casing.cement_top || ''}
                  onChange={(e) => onChange('cement_top', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Cement Yield (ft³/sk)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.01"
                  value={casing.cement_yield || ''}
                  onChange={(e) => onChange('cement_yield', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Burst (psi)</Form.Label>
                <Form.Control
                  type="number"
                  step="1"
                  value={casing.burst || ''}
                  onChange={(e) => onChange('burst', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Collapse (psi)</Form.Label>
                <Form.Control
                  type="number"
                  step="1"
                  value={casing.collapse || ''}
                  onChange={(e) => onChange('collapse', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Drift (in)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.001"
                  value={casing.drift || ''}
                  onChange={(e) => onChange('drift', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>Cancel</Button>
        <Button variant="primary" onClick={onSubmit}>
          {isEditing ? 'Update' : 'Add'} Casing
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CasingModal;