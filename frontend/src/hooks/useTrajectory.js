// src/hooks/useTrajectory.js
import { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toast } from 'react-toastify';
import {
  addTrajectoryPoint,
  updateTrajectoryPoint,
  selectPoint,
  clearSelection
} from '../store/slices/trajectorySlice';
import {
  validateTrajectoryPoint,
  calculateTrajectoryValues
} from '../utils/trajectoryValidation';

export const useTrajectory = (wellId) => {
  const dispatch = useDispatch();
  const trajectoryPoints = useSelector(state => state.trajectory.trajectoryPoints);
  const selectedPoint = useSelector(state => state.trajectory.selectedPoint);
  const [isCalculating, setIsCalculating] = useState(false);

  const validateAndCalculatePoint = useCallback((pointData) => {
    // Validate point data
    const errors = validateTrajectoryPoint(pointData, trajectoryPoints);
    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }

    // Find previous point if exists
    const previousPoint = trajectoryPoints.length > 0 ? 
      trajectoryPoints[trajectoryPoints.length - 1] : 
      null;

    // Calculate derived values
    return calculateTrajectoryValues(pointData, previousPoint);
  }, [trajectoryPoints]);

  const addPoint = useCallback(async (pointData) => {
    try {
      setIsCalculating(true);
      const calculatedPoint = validateAndCalculatePoint(pointData);
      
      await dispatch(addTrajectoryPoint({
        wellId,
        pointData: calculatedPoint
      })).unwrap();

      toast.success('Trajectory point added successfully');
    } catch (error) {
      toast.error(error.message || 'Failed to add trajectory point');
      throw error;
    } finally {
      setIsCalculating(false);
    }
  }, [dispatch, wellId, validateAndCalculatePoint]);

  const updatePoint = useCallback(async (pointId, pointData) => {
    try {
      setIsCalculating(true);
      const calculatedPoint = validateAndCalculatePoint(pointData);
      
      await dispatch(updateTrajectoryPoint({
        pointId,
        pointData: calculatedPoint
      })).unwrap();

      dispatch(clearSelection());
      toast.success('Trajectory point updated successfully');
    } catch (error) {
      toast.error(error.message || 'Failed to update trajectory point');
      throw error;
    } finally {
      setIsCalculating(false);
    }
  }, [dispatch, validateAndCalculatePoint]);

  const selectTrajectoryPoint = useCallback((point) => {
    dispatch(selectPoint(point));
  }, [dispatch]);

  const clearTrajectorySelection = useCallback(() => {
    dispatch(clearSelection());
  }, [dispatch]);

  // Return calculated values for visualization
  const getVisualizationData = useCallback(() => {
    if (!trajectoryPoints.length) return null;

    return {
      maxDepth: Math.max(...trajectoryPoints.map(p => p.measured_depth)),
      maxTVD: Math.max(...trajectoryPoints.map(p => p.true_vertical_depth)),
      maxHorizontalDisplacement: Math.max(...trajectoryPoints.map(p => p.vertical_section)),
      maxDLS: Math.max(...trajectoryPoints.map(p => p.dog_leg_severity))
    };
  }, [trajectoryPoints]);

  return {
    trajectoryPoints,
    selectedPoint,
    isCalculating,
    addPoint,
    updatePoint,
    selectTrajectoryPoint,
    clearTrajectorySelection,
    getVisualizationData
  };
};

export default useTrajectory;