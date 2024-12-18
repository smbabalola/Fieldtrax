// File: /frontend/src/components/settings/UnitPreview.jsx
import React from 'react';
import { Card, Form, Row, Col, Button, Alert } from 'react-bootstrap';
import { useSettings } from '../../hooks/useSettings';
import { REGION_PRESETS, UNIT_TYPES } from '../../constants';

const UnitPreview = () => {
  const {
    unitSystem,
    unitPreferences,
    loading,
    error,
    updateSettings
  } = useSettings();

  const handleUnitChange = async (type, value) => {
    try {
      await updateSettings({
        unitPreferences: {
          ...unitPreferences,
          [`${type}Unit`]: value
        }
      });
    } catch (err) {
      console.error('Failed to update unit:', err);
    }
  };

  const handleSystemChange = async (system) => {
    try {
      await updateSettings({
        unitSystem: system,
        unitPreferences: REGION_PRESETS[system]
      });
    } catch (err) {
      console.error('Failed to update unit system:', err);
    }
  };

  if (loading) {
    return (
      <Card>
        <Card.Body className="text-center p-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">Unit Preferences</h5>
      </Card.Header>
      <Card.Body>
        {error && (
          <Alert variant="danger" className="mb-4">
            {error}
          </Alert>
        )}

        <Form>
          {/* Unit System Selection */}
          <Form.Group className="mb-4">
            <Form.Label>Unit System</Form.Label>
            <div className="d-flex gap-2">
              <Button
                variant={unitSystem === 'US' ? 'primary' : 'outline-primary'}
                onClick={() => handleSystemChange('US')}
              >
                US
              </Button>
              <Button
                variant={unitSystem === 'METRIC' ? 'primary' : 'outline-primary'}
                onClick={() => handleSystemChange('METRIC')}
              >
                Metric
              </Button>
            </div>
          </Form.Group>

          {/* Individual Unit Settings */}
          <Row>
            {Object.entries(UNIT_TYPES).map(([type, units]) => (
              <Col md={6} key={type} className="mb-3">
                <Form.Group>
                  <Form.Label className="text-capitalize">
                    {type.replace('Unit', '')}
                  </Form.Label>
                  <Form.Select
                    value={unitPreferences[`${type}Unit`]}
                    onChange={(e) => handleUnitChange(type, e.target.value)}
                  >
                    {units.map(unit => (
                      <option key={unit} value={unit}>
                        {unit.toUpperCase()}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            ))}
          </Row>

          {/* Preview Section */}
          <div className="mt-4">
            <h6>Preview</h6>
            <div className="p-3 bg-light rounded">
              <small className="text-muted">Sample measurements in current units:</small>
              <ul className="list-unstyled mb-0 mt-2">
                <li>Length: 100 {unitPreferences.lengthUnit}</li>
                <li>Pressure: 2000 {unitPreferences.pressureUnit}</li>
                <li>Temperature: 75°{unitPreferences.temperatureUnit.toUpperCase()}</li>
                <li>Weight: 5000 {unitPreferences.weightUnit}</li>
                <li>Volume: 50 {unitPreferences.volumeUnit}</li>
                <li>Density: 8.6 {unitPreferences.densityUnit}</li>
                <li>Torque: 1000 {unitPreferences.torqueUnit}</li>
              </ul>
            </div>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default UnitPreview;