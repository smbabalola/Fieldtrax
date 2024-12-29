// src/utils/trajectoryValidation.js

export const validateTrajectoryPoint = (point, existingPoints = []) => {
    const errors = [];
  
    // Required field validation
    const requiredFields = {
      measured_depth: 'Measured Depth',
      inclination: 'Inclination',
      azimuth: 'Azimuth'
    };
  
    Object.entries(requiredFields).forEach(([field, label]) => {
      if (!point[field] && point[field] !== 0) {
        errors.push(`${label} is required`);
      }
    });
  
    // Numerical validation
    if (point.measured_depth < 0) {
      errors.push('Measured depth must be positive');
    }
  
    if (point.inclination < 0 || point.inclination > 180) {
      errors.push('Inclination must be between 0 and 180 degrees');
    }
  
    if (point.azimuth < 0 || point.azimuth > 360) {
      errors.push('Azimuth must be between 0 and 360 degrees');
    }
  
    // Sequential depth validation
    if (existingPoints.length > 0) {
      const lastPoint = existingPoints[existingPoints.length - 1];
      if (point.measured_depth <= lastPoint.measured_depth) {
        errors.push('Measured depth must be greater than previous point');
      }
    }
  
    return errors;
  };
  
  export const calculateTrajectoryValues = (point, previousPoint = null) => {
    const { measured_depth, inclination, azimuth } = point;
  
    // If this is the first point
    if (!previousPoint) {
      return {
        ...point,
        true_vertical_depth: measured_depth * Math.cos(inclination * Math.PI / 180),
        northing: measured_depth * Math.sin(inclination * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180),
        easting: measured_depth * Math.sin(inclination * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180),
        vertical_section: 0,
        dog_leg_severity: 0
      };
    }
  
    // Calculate values based on previous point
    const dMD = measured_depth - previousPoint.measured_depth;
    const dInc = inclination - previousPoint.inclination;
    const dAz = azimuth - previousPoint.azimuth;
  
    // Calculate TVD
    const tvd = previousPoint.true_vertical_depth + 
      (dMD * (Math.cos(inclination * Math.PI / 180) + Math.cos(previousPoint.inclination * Math.PI / 180)) / 2);
  
    // Calculate dog leg severity
    const dogLegAngle = Math.acos(
      Math.cos(previousPoint.inclination * Math.PI / 180) * Math.cos(inclination * Math.PI / 180) +
      Math.sin(previousPoint.inclination * Math.PI / 180) * Math.sin(inclination * Math.PI / 180) *
      Math.cos(dAz * Math.PI / 180)
    );
    const dls = (dogLegAngle * 180 / Math.PI) / (dMD / 100); // degrees per 100 ft
  
    // Calculate northing and easting
    const rf = dogLegAngle !== 0 ? 
      (2 / dogLegAngle) * Math.tan(dogLegAngle / 2) :
      1;
  
    const dN = (dMD / 2) * (
      Math.sin(previousPoint.inclination * Math.PI / 180) * Math.cos(previousPoint.azimuth * Math.PI / 180) +
      Math.sin(inclination * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180)
    ) * rf;
  
    const dE = (dMD / 2) * (
      Math.sin(previousPoint.inclination * Math.PI / 180) * Math.sin(previousPoint.azimuth * Math.PI / 180) +
      Math.sin(inclination * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180)
    ) * rf;
  
    const northing = previousPoint.northing + dN;
    const easting = previousPoint.easting + dE;
  
    // Calculate vertical section
    const vertical_section = Math.sqrt(Math.pow(northing, 2) + Math.pow(easting, 2));
  
    return {
      ...point,
      true_vertical_depth: tvd,
      northing,
      easting,
      vertical_section,
      dog_leg_severity: dls
    };
  };
  
  export const validateTrajectoryData = (trajectoryPoints) => {
    const errors = [];
  
    if (!trajectoryPoints || !Array.isArray(trajectoryPoints)) {
      errors.push('Invalid trajectory data format');
      return errors;
    }
  
    // Must have at least two points
    if (trajectoryPoints.length < 2) {
      errors.push('Trajectory must have at least two points');
      return errors;
    }
  
    // Validate each point and relationships between points
    trajectoryPoints.forEach((point, index) => {
      const pointErrors = validateTrajectoryPoint(point, trajectoryPoints.slice(0, index));
      if (pointErrors.length > 0) {
        errors.push(`Point ${index + 1}: ${pointErrors.join(', ')}`);
      }
    });
  
    return errors;
  };