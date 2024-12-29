// File: /src/components/jobs/CreateJob/modals/LinerModal.jsx
import React from 'react';
import { Modal, Form, Row, Col, Button } from 'react-bootstrap';
import { standardGrades, standardThreads } from '../../../../utils/tubularStandards';

const LinerModal = ({
  show,
  onHide,
  liner,
  onChange,
  onSubmit,
  isEditing
}) => {
  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{isEditing ? 'Edit Liner' : 'Add Liner'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          {/* Basic Properties - Similar to Casing */}
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Outer Diameter (in) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.001"
                  value={liner.outer_diameter || ''}
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
                  value={liner.inner_diameter || ''}
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
                  value={liner.weight || ''}
                  onChange={(e) => onChange('weight', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Grade <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={liner.grade || ''}
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

          {/* Liner-specific Properties */}
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Liner Top (ft) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.liner_top || ''}
                  onChange={(e) => onChange('liner_top', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Liner Bottom (ft) <span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.liner_bottom || ''}
                  onChange={(e) => onChange('liner_bottom', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>BHT at Liner Top (°F)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.bht_at_liner_top || ''}
                  onChange={(e) => onChange('bht_at_liner_top', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Liner Top Deviation (°)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.liner_top_deviation || ''}
                  onChange={(e) => onChange('liner_top_deviation', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Liner Shoe Deviation (°)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.liner_shoe_deviation || ''}
                  onChange={(e) => onChange('liner_shoe_deviation', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Liner Overlap Length (ft)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={liner.liner_Overlap_length || ''}
                  onChange={(e) => onChange('liner_Overlap_length', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          {/* Additional Properties */}
          <Row>
            <Col md={12}>
              <Form.Group className="mb-3">
                <Form.Label>Remarks</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={liner.remarks || ''}
                  onChange={(e) => onChange('remarks', e.target.value)}
                  placeholder="Enter any additional remarks or notes"
                />
              </Form.Group>
            </Col>
          </Row>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>Cancel</Button>
        <Button variant="primary" onClick={onSubmit}>
          {isEditing ? 'Update' : 'Add'} Liner
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LinerModal;