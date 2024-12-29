import React, { useState, useCallback } from 'react';
import { Card, Button, Form, Row, Col, Table } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaUpload, FaDownload, FaPlus, FaEdit, FaTrash, FaChartLine } from 'react-icons/fa';
import WellTrajectoryChart from '../../../Forms/WellTrajectoryChart';
import TrajectoryVisualizationControls from '../visualization/TrajectoryVisualizationControls';
import TrajectoryCalculations from '../visualization/TrajectoryCalculations';
import TrajectoryDataImportExport from '../modals/TrajectoryDataImportExport';
import useTrajectory from '../../../../hooks/useTrajectory';

const TrajectoryTab = ({ data, onUpdate }) => {
  const {
    trajectoryPoints,
    selectedPoint,
    isCalculating,
    addPoint,
    updatePoint,
    deletePoint,
    selectTrajectoryPoint,
    clearTrajectorySelection,
    getVisualizationData
  } = useTrajectory(data.well_id);

  // Local State
  const [showImportExport, setShowImportExport] = useState(false);
  const [visualizationMode, setVisualizationMode] = useState('2D');
  const [showGrid, setShowGrid] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [newPoint, setNewPoint] = useState({
    measured_depth: '',
    inclination: '',
    azimuth: '',
    true_vertical_depth: '',
    vertical_section: '',
    northing: '',
    easting: '',
    dog_leg_severity: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedPoint) {
        await updatePoint(selectedPoint.id, newPoint);
      } else {
        await addPoint(newPoint);
      }
      setNewPoint({
        measured_depth: '',
        inclination: '',
        azimuth: '',
        true_vertical_depth: '',
        vertical_section: '',
        northing: '',
        easting: '',
        dog_leg_severity: ''
      });
      onUpdate('trajectory', { trajectoryPoints });
    } catch (error) {
      toast.error(error.message);
    }
  };

  const handleImport = useCallback(async (importedData) => {
    try {
      // Clear existing points if needed
      for (const point of importedData) {
        await addPoint(point);
      }
      toast.success(`Successfully imported ${importedData.length} trajectory points`);
      onUpdate('trajectory', { trajectoryPoints: importedData });
    } catch (error) {
      toast.error(`Import failed: ${error.message}`);
    }
  }, [addPoint, onUpdate]);

  const handleDelete = async (pointId) => {
    try {
      await deletePoint(pointId);
      toast.success('Trajectory point deleted');
      clearTrajectorySelection();
    } catch (error) {
      toast.error(error.message);
    }
  };

  const handleVisualizationModeChange = (mode) => {
    setVisualizationMode(mode);
  };

  const handleToggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.querySelector('.well-trajectory-chart').requestFullscreen();
    } else {
      document.exitFullscreen();
    }
    setIsFullscreen(!isFullscreen);
  };

  return (
    <div className="trajectory-tab">
      {/* Trajectory Calculations */}
      <TrajectoryCalculations trajectoryData={trajectoryPoints} />

      {/* Data Entry Form */}
      <Card className="mb-4">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <h5 className="mb-0">Add Trajectory Point</h5>
          <div>
            <Button
              variant="outline-primary"
              size="sm"
              className="me-2"
              onClick={() => setShowImportExport(true)}
            >
              <FaUpload className="me-1" /> Import/Export
            </Button>
          </div>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Measured Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    value={newPoint.measured_depth}
                    onChange={(e) => setNewPoint(prev => ({
                      ...prev,
                      measured_depth: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Inclination (°)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0"
                    max="180"
                    value={newPoint.inclination}
                    onChange={(e) => setNewPoint(prev => ({
                      ...prev,
                      inclination: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Azimuth (°)</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0"
                    max="360"
                    value={newPoint.azimuth}
                    onChange={(e) => setNewPoint(prev => ({
                      ...prev,
                      azimuth: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Button
              type="submit"
              variant="primary"
              disabled={isCalculating}
            >
              {isCalculating ? 'Calculating...' : selectedPoint ? 'Update Point' : 'Add Point'}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {/* Visualization */}
      {trajectoryPoints.length > 0 && (
        <Card className="mb-4">
          <Card.Header>
            <TrajectoryVisualizationControls
              mode={visualizationMode}
              onModeChange={handleVisualizationModeChange}
              showGrid={showGrid}
              onToggleGrid={setShowGrid}
              showLabels={showLabels}
              onToggleLabels={setShowLabels}
              isFullscreen={isFullscreen}
              onToggleFullscreen={handleToggleFullscreen}
            />
          </Card.Header>
          <Card.Body>
            <WellTrajectoryChart
              trajectoryData={trajectoryPoints}
              mode={visualizationMode}
              showGrid={showGrid}
              showLabels={showLabels}
              onPointClick={(point) => {
                selectTrajectoryPoint(point);
                setNewPoint(point);
              }}
            />
          </Card.Body>
        </Card>
      )}

      {/* Data Table */}
      {trajectoryPoints.length > 0 && (
        <Table responsive striped bordered hover>
          <thead>
            <tr>
              <th>MD (ft)</th>
              <th>Inc (°)</th>
              <th>Az (°)</th>
              <th>TVD (ft)</th>
              <th>VS (ft)</th>
              <th>N/S (ft)</th>
              <th>E/W (ft)</th>
              <th>DLS (°/100ft)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {trajectoryPoints.map((point, index) => (
              <tr
                key={point.id || index}
                className={selectedPoint?.id === point.id ? 'table-primary' : ''}
              >
                <td>{point.measured_depth.toFixed(2)}</td>
                <td>{point.inclination.toFixed(2)}</td>
                <td>{point.azimuth.toFixed(2)}</td>
                <td>{point.true_vertical_depth.toFixed(2)}</td>
                <td>{point.vertical_section.toFixed(2)}</td>
                <td>{point.northing.toFixed(2)}</td>
                <td>{point.easting.toFixed(2)}</td>
                <td>{point.dog_leg_severity.toFixed(2)}</td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-1"
                    onClick={() => {
                      selectTrajectoryPoint(point);
                      setNewPoint(point);
                    }}
                  >
                    <FaEdit />
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(point.id)}
                  >
                    <FaTrash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Import/Export Modal */}
      <TrajectoryDataImportExport
        show={showImportExport}
        onHide={() => setShowImportExport(false)}
        onImport={handleImport}
        trajectoryData={trajectoryPoints}
      />
    </div>
  );
};

export default TrajectoryTab;