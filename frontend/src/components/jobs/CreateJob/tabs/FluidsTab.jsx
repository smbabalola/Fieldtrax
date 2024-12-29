// File: src/components/jobs/CreateJob/tabs/FluidsTab.jsx
import React, { useState, useEffect } from 'react';
import { Card, Form, Row, Col, Button, Table } from 'react-bootstrap';
import { toast } from 'react-toastify';

const FluidsTab = ({ data, onUpdate, errors = {} }) => {
  const [fluidData, setFluidData] = useState({
    type: 'drilling',
    density: '',
    viscosity: '',
    temperature: '',
    ph: '',
    gel_strength_10s: '',
    gel_strength_10m: '',
    test_results: [
      { location: '', test1: '', test2: '', test3: '', test4: '' },
      { location: '', test1: '', test2: '', test3: '', test4: '' },
      { location: '', test1: '', test2: '', test3: '', test4: '' }
    ],
    calculated: {
      yield_point: '',
      plastic_viscosity: ''
    }
  });

  // Handle basic property changes
  const handlePropertyChange = (property, value) => {
    setFluidData(prev => ({
      ...prev,
      [property]: value
    }));
  };

  // Handle test result changes
  const handleTestChange = (index, field, value) => {
    const updatedTests = [...fluidData.test_results];
    updatedTests[index] = {
      ...updatedTests[index],
      [field]: value
    };

    setFluidData(prev => ({
      ...prev,
      test_results: updatedTests
    }));
  };

  // Calculate properties based on test results
  useEffect(() => {
    const calculateProperties = () => {
      // Example calculations - replace with actual formulas
      const testAvg = fluidData.test_results.reduce((acc, test) => {
        const values = [test.test1, test.test2, test.test3, test.test4]
          .filter(val => val !== '')
          .map(Number);
        return values.length > 0 ? acc + (values.reduce((a, b) => a + b) / values.length) : acc;
      }, 0) / fluidData.test_results.filter(test => test.location !== '').length;

      // Simplified calculations - replace with actual formulas
      const calculated = {
        yield_point: testAvg * 0.5,
        plastic_viscosity: testAvg * 0.3,
        gel_strength: testAvg * 0.2
      };

      setFluidData(prev => ({
        ...prev,
        calculated
      }));
    };

    if (fluidData.test_results.some(test => test.location !== '')) {
      calculateProperties();
    }
  }, [fluidData.test_results]);

  // Update parent component when fluid data changes
  useEffect(() => {
    onUpdate('fluids', fluidData);
  }, [fluidData]);

  return (
    <div className="fluids-tab">
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">Fluid Properties</h5>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Fluid Type</Form.Label>
                <Form.Select
                  value={fluidData.type}
                  onChange={(e) => handlePropertyChange('type', e.target.value)}
                >
                  <option value="drilling">Drilling Fluid</option>
                  <option value="completion">Completion Fluid</option>
                  <option value="workover">Workover Fluid</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Density (ppg)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={fluidData.density}
                  onChange={(e) => handlePropertyChange('density', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Viscosity (cp)</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  value={fluidData.viscosity}
                  onChange={(e) => handlePropertyChange('viscosity', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Temperature (°F)</Form.Label>
                <Form.Control
                  type="number"
                  value={fluidData.temperature}
                  onChange={(e) => handlePropertyChange('temperature', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>pH</Form.Label>
                <Form.Control
                  type="number"
                  step="0.1"
                  min="0"
                  max="14"
                  value={fluidData.ph}
                  onChange={(e) => handlePropertyChange('ph', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">Test Results</h5>
        </Card.Header>
        <Card.Body>
          <Table responsive>
            <thead>
              <tr>
                <th>Location</th>
                <th>Test 1</th>
                <th>Test 2</th>
                <th>Test 3</th>
                <th>Test 4</th>
              </tr>
            </thead>
            <tbody>
              {fluidData.test_results.map((test, index) => (
                <tr key={index}>
                  <td>
                    <Form.Control
                      type="text"
                      value={test.location}
                      onChange={(e) => handleTestChange(index, 'location', e.target.value)}
                      placeholder="Enter location"
                    />
                  </td>
                  <td>
                    <Form.Control
                      type="number"
                      step="0.1"
                      value={test.test1}
                      onChange={(e) => handleTestChange(index, 'test1', e.target.value)}
                    />
                  </td>
                  <td>
                    <Form.Control
                      type="number"
                      step="0.1"
                      value={test.test2}
                      onChange={(e) => handleTestChange(index, 'test2', e.target.value)}
                    />
                  </td>
                  <td>
                    <Form.Control
                      type="number"
                      step="0.1"
                      value={test.test3}
                      onChange={(e) => handleTestChange(index, 'test3', e.target.value)}
                    />
                  </td>
                  <td>
                    <Form.Control
                      type="number"
                      step="0.1"
                      value={test.test4}
                      onChange={(e) => handleTestChange(index, 'test4', e.target.value)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      <Card>
        <Card.Header>
          <h5 className="mb-0">Calculated Properties</h5>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Yield Point (lbf/100ft²)</Form.Label>
                <Form.Control
                  type="number"
                  value={fluidData.calculated.yield_point}
                  readOnly
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Plastic Viscosity (cp)</Form.Label>
                <Form.Control
                  type="number"
                  value={fluidData.calculated.plastic_viscosity}
                  readOnly
                />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group className="mb-3">
                <Form.Label>Gel Strength (lbf/100ft²)</Form.Label>
                <Form.Control
                  type="number"
                  value={fluidData.calculated.gel_strength}
                  readOnly
                />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </div>
  );
};

export default FluidsTab;