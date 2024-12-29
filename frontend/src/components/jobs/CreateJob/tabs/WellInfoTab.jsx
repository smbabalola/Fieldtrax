// File: /src/components/jobs/CreateJob/tabs/WellInfoTab.jsx
import React, { useState, useEffect } from 'react';
import { Form, Row, Col, Card, Button } from 'react-bootstrap';
import { DataTable } from '../../../common/DataTable';
import wellService from '../../../../services/wellService';
import WellDetailModal from '../../../wells/WellDetailModal';
import { toast } from 'react-toastify';

const WellInfoTab = ({ data, onChange, errors = {} }) => {
  // State
  const [loading, setLoading] = useState(false);
  const [wells, setWells] = useState([]);
  const [wellShapes, setWellShapes] = useState([]);
  const [productionTypes, setProductionTypes] = useState([]);
  const [slots, setSlots] = useState([]);
  const [showWellModal, setShowWellModal] = useState(false);
  const [selectedWell, setSelectedWell] = useState(null);
  const [error, setError] = useState(null);

  // Table Columns Definition
  const columns = [
    { field: 'well_name', header: 'Well Name', sortable: true },
    { field: 'api_number', header: 'API Number', sortable: true },
    { field: 'field_name', header: 'Field Name', sortable: true },
    { field: 'location', header: 'Location', sortable: true },
    { field: 'county', header: 'County', sortable: true },
    { field: 'state', header: 'State', sortable: true }
  ];

  // Handler for updating form data
  const handleUpdate = (updates) => {
    if (!onChange) {
      console.warn('onChange function not provided to WellInfoTab');
      return;
    }

    try {
      const updatedData = {
        ...data,
        ...updates
      };
      console.log('Updating well data:', updatedData);
      onChange(updatedData);
    } catch (err) {
      console.error('Error updating data:', err);
      toast.error('Failed to update well information');
    }
  };

  // Fetch Wells
  useEffect(() => {
    const fetchWells = async () => {
      if (!data.operator_id) return;
      
      try {
        setLoading(true);
        setError(null);
        const response = await wellService.getWellsByOperator(data.operator_id); // Ensure this function exists in wellService
        setWells(Array.isArray(response) ? response : []);
      } catch (error) {
        console.error('Error fetching wells:', error);
        setError('Failed to load wells');
        toast.error('Failed to load wells list');
      } finally {
        setLoading(false);
      }
    };

    fetchWells();
  }, [data.operator_id]);

  // Fetch reference data
  useEffect(() => {
    const fetchReferenceData = async () => {
      try {
        const [shapes, productions, slotsList] = await Promise.all([
          wellService.getWellShapes(), // Ensure this function exists in wellService
          wellService.getProductionTypes(), // Ensure this function exists in wellService
          wellService.getSlots() // Ensure this function exists in wellService
        ]);
        
        setWellShapes(shapes);
        setProductionTypes(productions);
        setSlots(slotsList);
      } catch (error) {
        console.error('Error fetching reference data:', error);
        toast.error('Failed to load reference data');
      }
    };

    fetchReferenceData();
  }, []);

  // Handlers
  const handleInputChange = (field, value) => {
    handleUpdate({ [field]: value });
  };

  const handleCheckboxChange = (field) => {
    handleUpdate({ [field]: !data[field] });
  };

  const handleWellSelect = (well) => {
    if (!well) return;
    
    console.log('Selected well:', well);
    handleUpdate({
      well_id: well.id,
      well_name: well.well_name,
      field_name: well.field_name,
      api_number: well.api_number,
      location: well.location,
      county: well.county,
      state: well.state
    });
    
    toast.success(`Selected well: ${well.well_name}`);
  };

  const handleWellAdded = (newWell) => {
    setWells(prev => [...prev, newWell]);
    handleWellSelect(newWell);
    setShowWellModal(false);
    toast.success('Well added successfully');
  };

  return (
    <div>
      <Card className="mb-4">
        <Card.Body>
          <Row>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Selected Well <span className="text-danger">*</span></Form.Label>
                <div className="d-flex gap-2">
                  <Form.Control
                    type="text"
                    value={wells.find(w => w.id === data.well_id)?.well_name || ''}
                    readOnly
                    placeholder="Select a well from the table below"
                    isInvalid={!!errors.well_id}
                  />
                  <Button
                    variant="outline-primary"
                    onClick={() => {
                      setSelectedWell(null);
                      setShowWellModal(true);
                    }}
                    disabled={!data.operator_id}
                  >
                    Add New
                  </Button>
                </div>
                <Form.Control.Feedback type="invalid">
                  {errors.well_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>

            <Col md={6}>
              <Form.Group>
                <Form.Label>Field Name</Form.Label>
                <Form.Control
                  type="text"
                  value={data.field_name || ''}
                  readOnly
                  isInvalid={!!errors.field_name}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row className="mt-3">
            {/* Well Shape Selection */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Well Shape <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.well_shape_id || ''}
                  onChange={(e) => handleInputChange('well_shape_id', e.target.value)}
                  isInvalid={!!errors.well_shape_id}
                >
                  <option value="">Select Well Shape</option>
                  {wellShapes.map(shape => (
                    <option key={shape.id} value={shape.id}>
                      {shape.well_shape}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.well_shape_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>

            {/* Production Type Selection */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Production Type <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.production_id || ''}
                  onChange={(e) => handleInputChange('production_id', e.target.value)}
                  isInvalid={!!errors.production_id}
                >
                  <option value="">Select Production Type</option>
                  {productionTypes.map(type => (
                    <option key={type.id} value={type.id}>
                      {type.production_type}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.production_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            {/* Slot Selection */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Slot <span className="text-danger">*</span></Form.Label>
                <Form.Select
                  value={data.slot_id || ''}
                  onChange={(e) => handleInputChange('slot_id', e.target.value)}
                  isInvalid={!!errors.slot_id}
                >
                  <option value="">Select Slot</option>
                  {slots.map(slot => (
                    <option key={slot.id} value={slot.id}>
                      {slot.slot_name}
                    </option>
                  ))}
                </Form.Select>
                <Form.Control.Feedback type="invalid">
                  {errors.slot_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>

            {/* Measured Depth */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Measured Depth (ft)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.01"
                  value={data.measured_depth || ''}
                  onChange={(e) => handleInputChange('measured_depth', e.target.value)}
                  placeholder="Enter measured depth"
                  isInvalid={!!errors.measured_depth}
                />
                <Form.Control.Feedback type="invalid">
                  {errors.measured_depth}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>

          <Row>
            {/* Total Vertical Depth */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Total Vertical Depth (ft)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.01"
                  value={data.total_vertical_depth || ''}
                  onChange={(e) => handleInputChange('total_vertical_depth', e.target.value)}
                  placeholder="Enter total vertical depth"
                  isInvalid={!!errors.total_vertical_depth}
                />
                <Form.Control.Feedback type="invalid">
                  {errors.total_vertical_depth}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>

            {/* H2S and CO2 Checkboxes */}
            <Col md={6}>
              <div className="mt-4">
                <Form.Check
                  type="switch"
                  id="h2s-switch"
                  label="H2S Present"
                  checked={data.h2s || false}
                  onChange={() => handleCheckboxChange('h2s')}
                  className="mb-2"
                />
                <Form.Check
                  type="switch"
                  id="co2-switch"
                  label="CO2 Present"
                  checked={data.co2 || false}
                  onChange={() => handleCheckboxChange('co2')}
                />
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <DataTable
        columns={columns}
        data={wells}
        loading={loading}
        onRowClick={handleWellSelect}
        selectedId={data.well_id}
      />

      <WellDetailModal
        show={showWellModal}
        onHide={() => setShowWellModal(false)}
        operatorId={data.operator_id}
        well={selectedWell}
        onWellAdded={handleWellAdded}
      />
    </div>
  );
};

export default WellInfoTab;