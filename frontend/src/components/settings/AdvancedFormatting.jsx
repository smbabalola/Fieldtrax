// File: /frontend/src/components/settings/AdvancedFormatting.jsx
import React from 'react';
import { Card, Form, Row, Col, Alert } from 'react-bootstrap';
import { useSettings } from '../../hooks/useSettings';

const AdvancedFormatting = () => {
  const {
    displaySettings,
    loading,
    error,
    updateSettings
  } = useSettings();

  const handleDisplayChange = async (setting, value) => {
    try {
      await updateSettings({
        displaySettings: {
          ...displaySettings,
          [setting]: value
        }
      });
    } catch (err) {
      console.error('Failed to update display settings:', err);
    }
  };

  const handleDecimalPlacesChange = async (type, value) => {
    const numValue = parseInt(value, 10);
    if (isNaN(numValue) || numValue < 0 || numValue > 6) return;

    try {
      await updateSettings({
        displaySettings: {
          ...displaySettings,
          decimalPlaces: {
            ...displaySettings.decimalPlaces,
            [type]: numValue
          }
        }
      });
    } catch (err) {
      console.error('Failed to update decimal places:', err);
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
        <h5 className="mb-0">Display Settings</h5>
      </Card.Header>
      <Card.Body>
        {error && (
          <Alert variant="danger" className="mb-4">
            {error}
          </Alert>
        )}

        <Form>
          {/* General Display Settings */}
          <div className="mb-4">
            <h6>General</h6>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
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
                <Form.Group className="mt-2">
                  <Form.Check
                    type="switch"
                    id="darkMode"
                    label="Dark Mode"
                    checked={displaySettings.darkMode}
                    onChange={(e) => handleDisplayChange('darkMode', e.target.checked)}
                  />
                  <Form.Check
                    type="switch"
                    id="highContrast"
                    label="High Contrast"
                    checked={displaySettings.highContrast}
                    onChange={(e) => handleDisplayChange('highContrast', e.target.checked)}
                  />
                </Form.Group>
              </Col>
            </Row>
          </div>

          {/* Decimal Places */}
          <div>
            <h6>Decimal Places</h6>
            <Row>
              {Object.entries(displaySettings.decimalPlaces).map(([type, value]) => (
                <Col md={4} key={type} className="mb-3">
                  <Form.Group>
                    <Form.Label className="text-capitalize">
                      {type}
                    </Form.Label>
                    <Form.Control
                      type="number"
                      min="0"
                      max="6"
                      value={value}
                      onChange={(e) => handleDecimalPlacesChange(type, e.target.value)}
                    />
                  </Form.Group>
                </Col>
              ))}
            </Row>
          </div>

          {/* Preview Section */}
          <div className="mt-4">
            <h6>Preview</h6>
            <div 
              className={`p-3 rounded ${displaySettings.darkMode ? 'bg-dark text-light' : 'bg-light'}`}
              style={{
                fontSize: {
                  small: '0.875rem',
                  medium: '1rem',
                  large: '1.125rem'
                }[displaySettings.fontSize]
              }}
            >
              <p className="mb-2">Sample text with current settings</p>
              <ul className="list-unstyled mb-0">
                <li>Length: {(123.456).toFixed(displaySettings.decimalPlaces.length)} ft</li>
                <li>Pressure: {(2000.789).toFixed(displaySettings.decimalPlaces.pressure)} psi</li>
                <li>Temperature: {(98.6).toFixed(displaySettings.decimalPlaces.temperature)}°F</li>
                <li>Weight: {(5000.123).toFixed(displaySettings.decimalPlaces.weight)} lbs</li>
              </ul>
            </div>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default AdvancedFormatting;