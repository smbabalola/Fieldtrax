
//===============================================
// File: /frontend/src/components/settings/SettingsPanel.jsx
//===============================================
import React from 'react';
import { Card, Form, Row, Col, Button } from 'react-bootstrap';
import { useSettings } from '../../hooks/useSettings';

const SettingsPanel = () => {
  const {
    unitPreferences,
    displaySettings,
    updateUnits,
    updateDisplay,
    loading,
    error,
    getAvailableUnits
  } = useSettings();

  const handleUnitChange = (type, value) => {
    updateUnits({ [`${type}Unit`]: value });
  };

  const handleDisplayChange = (setting, value) => {
    updateDisplay({ [setting]: value });
  };

  if (loading) return <div>Loading settings...</div>;
  if (error) return <div>Error loading settings: {error}</div>;

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">Settings</h5>
      </Card.Header>
      <Card.Body>
        <Form>
          <h6 className="mb-3">Unit Preferences</h6>
          <Row className="g-3">
            {Object.entries(unitPreferences).map(([type, currentUnit]) => (
              <Col md={6} key={type}>
                <Form.Group>
                  <Form.Label>{type.replace('Unit', '').toUpperCase()}</Form.Label>
                  <Form.Select
                    value={currentUnit}
                    onChange={(e) => handleUnitChange(type, e.target.value)}
                  >
                    {getAvailableUnits(type).map(unit => (
                      <option key={unit} value={unit}>
                        {unit.toUpperCase()}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            ))}
          </Row>

          <h6 className="mb-3 mt-4">Display Settings</h6>
          <Row className="g-3">
            <Col md={6}>
              <Form.Group>
                <Form.Label>Font Size</Form.Label>
                <Form.Select
                  value={displaySettings.fontSize}
                  onChange={(e) => handleDisplayChange('fontSize', e.target.value)}
                >
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mt-4">
                <Form.Check
                  type="switch"
                  id="darkMode"
                  label="Dark Mode"
                  checked={displaySettings.darkMode}
                  onChange={(e) => handleDisplayChange('darkMode', e.target.checked)}
                />
              </Form.Group>
            </Col>
          </Row>
        </Form>
      </Card.Body>
    </Card>
  );
};
