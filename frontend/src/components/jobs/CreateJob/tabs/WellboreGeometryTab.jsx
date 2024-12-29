// frontend\src\components\jobs\CreateJob\tabs\WellboreGeometryTab.jsx
import React, { useState, useEffect } from 'react';
import { Form, Row, Col, Card, Button, Modal, Table } from 'react-bootstrap';
import { FaPlus, FaTrash, FaEdit } from 'react-icons/fa';
import { toast } from 'react-toastify';

const WellboreGeometryTab = ({ data, onUpdate, errors = {} }) => {
  // State Management
  const [casings, setCasings] = useState(data.wellbore_geometry?.casings || []);
  const [liners, setLiners] = useState(data.wellbore_geometry?.liners || []);
  const [showCasingModal, setShowCasingModal] = useState(false);
  const [showLinerModal, setShowLinerModal] = useState(false);
  const [selectedCasing, setSelectedCasing] = useState(null);
  const [selectedLiner, setSelectedLiner] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);

  // Form States
  const [newCasing, setNewCasing] = useState({
    outer_diameter: '',
    inner_diameter: '',
    weight: '',
    grade: '',
    thread: '',
    open_hole_size: '',
    start_depth: '',
    end_depth: '',
    cement_top: '',
    cement_yield: ''
  });

  const [newLiner, setNewLiner] = useState({
    outer_diameter: '',
    inner_diameter: '',
    weight: '',
    grade: '',
    thread: '',
    open_hole_size: '',
    start_depth: '',
    end_depth: '',
    liner_top: '',
    liner_bottom: '',
    liner_overlap_length: ''
  });

  // Update parent component when casings or liners change
  useEffect(() => {
    onUpdate('wellbore_geometry', {
      casings,
      liners
    });
  }, [casings, liners]);

  // Validation Functions
  const validateCasing = (casing) => {
    const errors = [];
    
    if (!casing.outer_diameter) errors.push('Outer diameter is required');
    if (!casing.inner_diameter) errors.push('Inner diameter is required');
    if (!casing.weight) errors.push('Weight is required');
    if (!casing.grade) errors.push('Grade is required');
    
    if (parseFloat(casing.inner_diameter) >= parseFloat(casing.outer_diameter)) {
      errors.push('Inner diameter must be less than outer diameter');
    }
    
    if (casing.start_depth && casing.end_depth && 
        parseFloat(casing.start_depth) >= parseFloat(casing.end_depth)) {
      errors.push('Start depth must be less than end depth');
    }

    // Check for overlapping casings
    const otherCasings = casings.filter(c => c.id !== (selectedCasing?.id || ''));
    const hasOverlap = otherCasings.some(existing => {
      const newStart = parseFloat(casing.start_depth);
      const newEnd = parseFloat(casing.end_depth);
      const existingStart = parseFloat(existing.start_depth);
      const existingEnd = parseFloat(existing.end_depth);

      return (newStart >= existingStart && newStart <= existingEnd) ||
             (newEnd >= existingStart && newEnd <= existingEnd);
    });

    if (hasOverlap) {
      errors.push('Depth range overlaps with existing casing');
    }

    return errors;
  };

  const validateLiner = (liner) => {
    const errors = [];
    
    if (!liner.outer_diameter) errors.push('Outer diameter is required');
    if (!liner.inner_diameter) errors.push('Inner diameter is required');
    if (!liner.weight) errors.push('Weight is required');
    if (!liner.grade) errors.push('Grade is required');
    
    if (parseFloat(liner.inner_diameter) >= parseFloat(liner.outer_diameter)) {
      errors.push('Inner diameter must be less than outer diameter');
    }
    
    if (liner.start_depth && liner.end_depth && 
        parseFloat(liner.start_depth) >= parseFloat(liner.end_depth)) {
      errors.push('Start depth must be less than end depth');
    }

    // Validate liner fits inside casing
    const parentCasing = casings.find(casing => 
      parseFloat(liner.start_depth) >= parseFloat(casing.start_depth) && 
      parseFloat(liner.start_depth) <= parseFloat(casing.end_depth)
    );

    if (!parentCasing) {
      errors.push('Liner must start within an existing casing');
    } else if (parseFloat(liner.outer_diameter) >= parseFloat(parentCasing.inner_diameter)) {
      errors.push('Liner outer diameter must be less than parent casing inner diameter');
    }

    return errors;
  };

  // Handlers
  const handleAddCasing = () => {
    const validationErrors = validateCasing(newCasing);
    
    if (validationErrors.length > 0) {
      validationErrors.forEach(error => toast.error(error));
      return;
    }

    try {
      if (isEditMode && selectedCasing) {
        const updatedCasings = casings.map(casing =>
          casing.id === selectedCasing.id ? { ...casing, ...newCasing } : casing
        );
        setCasings(updatedCasings);
        toast.success('Casing updated successfully');
      } else {
        const newId = Date.now().toString();
        setCasings([...casings, { ...newCasing, id: newId }]);
        toast.success('Casing added successfully');
      }
      
      handleCloseCasingModal();
    } catch (error) {
      toast.error('Error saving casing');
      console.error('Error saving casing:', error);
    }
  };

  const handleAddLiner = () => {
    const validationErrors = validateLiner(newLiner);
    
    if (validationErrors.length > 0) {
      validationErrors.forEach(error => toast.error(error));
      return;
    }

    try {
      if (isEditMode && selectedLiner) {
        const updatedLiners = liners.map(liner =>
          liner.id === selectedLiner.id ? { ...liner, ...newLiner } : liner
        );
        setLiners(updatedLiners);
        toast.success('Liner updated successfully');
      } else {
        const newId = Date.now().toString();
        setLiners([...liners, { ...newLiner, id: newId }]);
        toast.success('Liner added successfully');
      }
      
      handleCloseLinerModal();
    } catch (error) {
      toast.error('Error saving liner');
      console.error('Error saving liner:', error);
    }
  };

  const handleDeleteCasing = (casingId) => {
    try {
      const updatedCasings = casings.filter(casing => casing.id !== casingId);
      setCasings(updatedCasings);
      toast.success('Casing deleted successfully');
    } catch (error) {
      toast.error('Error deleting casing');
      console.error('Error deleting casing:', error);
    }
  };

  const handleDeleteLiner = (linerId) => {
    try {
      const updatedLiners = liners.filter(liner => liner.id !== linerId);
      setLiners(updatedLiners);
      toast.success('Liner deleted successfully');
    } catch (error) {
      toast.error('Error deleting liner');
      console.error('Error deleting liner:', error);
    }
  };

  // Modal Handlers
  const handleOpenCasingModal = (casing = null) => {
    if (casing) {
      setSelectedCasing(casing);
      setNewCasing(casing);
      setIsEditMode(true);
    } else {
      setSelectedCasing(null);
      setNewCasing({
        outer_diameter: '',
        inner_diameter: '',
        weight: '',
        grade: '',
        thread: '',
        open_hole_size: '',
        start_depth: '',
        end_depth: '',
        cement_top: '',
        cement_yield: ''
      });
      setIsEditMode(false);
    }
    setShowCasingModal(true);
  };

  const handleOpenLinerModal = (liner = null) => {
    if (liner) {
      setSelectedLiner(liner);
      setNewLiner(liner);
      setIsEditMode(true);
    } else {
      setSelectedLiner(null);
      setNewLiner({
        outer_diameter: '',
        inner_diameter: '',
        weight: '',
        grade: '',
        thread: '',
        open_hole_size: '',
        start_depth: '',
        end_depth: '',
        liner_top: '',
        liner_bottom: '',
        liner_overlap_length: ''
      });
      setIsEditMode(false);
    }
    setShowLinerModal(true);
  };

  const handleCloseCasingModal = () => {
    setShowCasingModal(false);
    setSelectedCasing(null);
    setNewCasing({
      outer_diameter: '',
      inner_diameter: '',
      weight: '',
      grade: '',
      thread: '',
      open_hole_size: '',
      start_depth: '',
      end_depth: '',
      cement_top: '',
      cement_yield: ''
    });
    setIsEditMode(false);
  };

  const handleCloseLinerModal = () => {
    setShowLinerModal(false);
    setSelectedLiner(null);
    setNewLiner({
      outer_diameter: '',
      inner_diameter: '',
      weight: '',
      grade: '',
      thread: '',
      open_hole_size: '',
      start_depth: '',
      end_depth: '',
      liner_top: '',
      liner_bottom: '',
      liner_overlap_length: ''
    });
    setIsEditMode(false);
  };

  return (
    <div className="wellbore-geometry-tab">
      {/* Casings Section */}
      <Card className="mb-4">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Casings</h5>
          <Button
            variant="primary"
            size="sm"
            onClick={() => handleOpenCasingModal()}
          >
            <FaPlus className="me-2" />
            Add Casing
          </Button>
        </Card.Header>
        <Card.Body>
          <Table responsive striped bordered hover>
            <thead>
              <tr>
                <th>OD (in)</th>
                <th>ID (in)</th>
                <th>Weight (lbs/ft)</th>
                <th>Grade</th>
                <th>Start Depth (ft)</th>
                <th>End Depth (ft)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {casings.map((casing) => (
                <tr key={casing.id}>
                  <td>{casing.outer_diameter}</td>
                  <td>{casing.inner_diameter}</td>
                  <td>{casing.weight}</td>
                  <td>{casing.grade}</td>
                  <td>{casing.start_depth}</td>
                  <td>{casing.end_depth}</td>
                  <td>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      className="me-2"
                      onClick={() => handleOpenCasingModal(casing)}
                    >
                      <FaEdit />
                    </Button>
                    <Button
                      variant="outline-danger"
                      size="sm"
                      onClick={() => handleDeleteCasing(casing.id)}
                    >
                      <FaTrash />
                    </Button>
                  </td>
                </tr>
              ))}
              {casings.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center">
                    No casings added yet
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Liners Section */}
      <Card>
        <Card.Header className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Liners</h5>
          <Button
            variant="primary"
            size="sm"
            onClick={() => handleOpenLinerModal()}
          >
            <FaPlus className="me-2" />
            Add Liner
          </Button>
        </Card.Header>
        <Card.Body>
          <Table responsive striped bordered hover>
            <thead>
              <tr>
                <th>OD (in)</th>
                <th>ID (in)</th>
                <th>Weight (lbs/ft)</th>
                <th>Grade</th>
                <th>Start Depth (ft)</th>
                <th>End Depth (ft)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {liners.map((liner) => (
                <tr key={liner.id}>
                  <td>{liner.outer_diameter}</td>
                  <td>{liner.inner_diameter}</td>
                  <td>{liner.weight}</td>
                  <td>{liner.grade}</td>
                  <td>{liner.start_depth}</td>
                  <td>{liner.end_depth}</td>
                  <td>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      className="me-2"
                      onClick={() => handleOpenLinerModal(liner)}
                    >
                      <FaEdit />
                    </Button>
                    <Button
                      variant="outline-danger"
                      size="sm"
                      onClick={() => handleDeleteLiner(liner.id)}
                    >
                      <FaTrash />
                    </Button>
                  </td>
                </tr>
              ))}
              {liners.length === 0 && (
                <tr>
                  <td colSpan="7" className="text-center">
                    No liners added yet
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Casing Modal */}
      <Modal show={showCasingModal} onHide={handleCloseCasingModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{isEditMode ? 'Edit Casing' : 'Add Casing'}</Modal.Title>
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
                    value={newCasing.outer_diameter}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      outer_diameter: e.target.value
                    }))}
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
                    value={newCasing.inner_diameter}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      inner_diameter: e.target.value
                    }))}
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
                    value={newCasing.weight}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      weight: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Grade <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    value={newCasing.grade}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      grade: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Thread</Form.Label>
                  <Form.Control
                    type="text"
                    value={newCasing.thread}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      thread: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Open Hole Size (in)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.001"
                    value={newCasing.open_hole_size}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      open_hole_size: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newCasing.start_depth}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      start_depth: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>End Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newCasing.end_depth}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      end_depth: e.target.value
                    }))}
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
                    value={newCasing.cement_top}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      cement_top: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Cement Yield (cu ft/sack)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    value={newCasing.cement_yield}
                    onChange={(e) => setNewCasing(prev => ({
                      ...prev,
                      cement_yield: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseCasingModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleAddCasing}>
            {isEditMode ? 'Update' : 'Add'} Casing
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Liner Modal */}
      <Modal show={showLinerModal} onHide={handleCloseLinerModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>{isEditMode ? 'Edit Liner' : 'Add Liner'}</Modal.Title>
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
                    value={newLiner.outer_diameter}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      outer_diameter: e.target.value
                    }))}
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
                    value={newLiner.inner_diameter}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      inner_diameter: e.target.value
                    }))}
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
                    value={newLiner.weight}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      weight: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Grade <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    value={newLiner.grade}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      grade: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Thread</Form.Label>
                  <Form.Control
                    type="text"
                    value={newLiner.thread}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      thread: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Open Hole Size (in)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.001"
                    value={newLiner.open_hole_size}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      open_hole_size: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newLiner.start_depth}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      start_depth: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>End Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newLiner.end_depth}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      end_depth: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Liner Top (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newLiner.liner_top}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      liner_top: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Liner Bottom (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newLiner.liner_bottom}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      liner_bottom: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Overlap Length (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.1"
                    value={newLiner.liner_overlap_length}
                    onChange={(e) => setNewLiner(prev => ({
                      ...prev,
                      liner_overlap_length: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseLinerModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleAddLiner}>
            {isEditMode ? 'Update' : 'Add'} Liner
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default WellboreGeometryTab;