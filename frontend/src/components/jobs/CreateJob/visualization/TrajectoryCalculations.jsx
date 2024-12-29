import React, { useMemo } from 'react';
import { Card, Row, Col } from 'react-bootstrap';
import { 
  FaRuler, 
  FaAngleDoubleDown, 
  FaCompass, 
  FaArrowsAlt,
  FaChartLine
} from 'react-icons/fa';

const TrajectoryCalculations = ({ trajectoryData }) => {
  const calculations = useMemo(() => {
    if (!trajectoryData?.length) return null;

    const lastPoint = trajectoryData[trajectoryData.length - 1];
    const maxInclination = Math.max(...trajectoryData.map(p => p.inclination));
    const maxDLS = Math.max(...trajectoryData.map(p => p.dog_leg_severity));
    
    // Calculate build rate (rate of inclination change)
    const buildRates = trajectoryData.slice(1).map((point, index) => {
      const prevPoint = trajectoryData[index];
      const depthDiff = point.measured_depth - prevPoint.measured_depth;
      const inclinationDiff = point.inclination - prevPoint.inclination;
      return (inclinationDiff / depthDiff) * 100; // degrees per 100ft
    });
    
    const avgBuildRate = buildRates.reduce((a, b) => a + b, 0) / buildRates.length;

    // Calculate total displacement
    const totalDisplacement = Math.sqrt(
      Math.pow(lastPoint.northing, 2) + 
      Math.pow(lastPoint.easting, 2)
    );

    // Calculate vertical section azimuth
    const vsAzimuth = Math.atan2(lastPoint.easting, lastPoint.northing) * 180 / Math.PI;

    return {
      totalMD: lastPoint.measured_depth,
      totalTVD: lastPoint.true_vertical_depth,
      totalDisplacement,
      vsAzimuth: vsAzimuth < 0 ? vsAzimuth + 360 : vsAzimuth,
      maxInclination,
      avgBuildRate,
      maxDLS,
      totalNS: lastPoint.northing,
      totalEW: lastPoint.easting,
      kdRatio: lastPoint.true_vertical_depth / totalDisplacement
    };
  }, [trajectoryData]);

  if (!calculations) return null;

  return (
    <Card className="mb-4">
      <Card.Header>
        <h5 className="mb-0">Trajectory Calculations</h5>
      </Card.Header>
      <Card.Body>
        <Row>
          <Col md={6} lg={4} className="mb-3">
            <div className="d-flex align-items-center mb-2">
              <FaRuler className="me-2 text-primary" />
              <h6 className="mb-0">Depth Measurements</h6>
            </div>
            <div className="ms-4">
              <p className="mb-1">Total MD: {calculations.totalMD.toFixed(2)} ft</p>
              <p className="mb-1">Total TVD: {calculations.totalTVD.toFixed(2)} ft</p>
              <p className="mb-0">Total VS: {calculations.totalDisplacement.toFixed(2)} ft</p>
            </div>
          </Col>

          <Col md={6} lg={4} className="mb-3">
            <div className="d-flex align-items-center mb-2">
              <FaAngleDouble Down className="me-2 text-primary" />
              <h6 className="mb-0">Inclination Data</h6>
            </div>
            <div className="ms-4">
              <p className="mb-1">Max Inclination: {calculations.maxInclination.toFixed(2)}°</p>
              <p className="mb-1">Avg Build Rate: {calculations.avgBuildRate.toFixed(2)}°/100ft</p>
              <p className="mb-0">Max DLS: {calculations.maxDLS.toFixed(2)}°/100ft</p>
            </div>
          </Col>

          <Col md={6} lg={4} className="mb-3">
            <div className="d-flex align-items-center mb-2">
              <FaCompass className="me-2 text-primary" />
              <h6 className="mb-0">Directional Data</h6>
            </div>
            <div className="ms-4">
              <p className="mb-1">VS Azimuth: {calculations.vsAzimuth.toFixed(2)}°</p>
              <p className="mb-1">N/S: {calculations.totalNS.toFixed(2)} ft</p>
              <p className="mb-0">E/W: {calculations.totalEW.toFixed(2)} ft</p>
            </div>
          </Col>

          <Col md={6} lg={4} className="mb-3">
            <div className="d-flex align-items-center mb-2">
              <FaChartLine className="me-2 text-primary" />
              <h6 className="mb-0">Analysis</h6>
            </div>
            <div className="ms-4">
              <p className="mb-1">K/D Ratio: {calculations.kdRatio.toFixed(3)}</p>
              <p className="mb-0">Complexity Index: {(calculations.maxDLS * calculations.maxInclination / 100).toFixed(2)}</p>
            </div>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default TrajectoryCalculations;