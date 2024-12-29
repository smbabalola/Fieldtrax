// src/hooks/useNavigation.js
import { useState, useCallback, useMemo } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const useNavigation = (steps, baseUrl, validationSchema) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isNavigating, setIsNavigating] = useState(false);
  
  // Get current step index based on URL
  const currentStepIndex = useMemo(() => {
    const currentPath = location.pathname.replace(baseUrl, '');
    return steps.findIndex(step => step.path === currentPath) || 0;
  }, [location.pathname, steps, baseUrl]);

  // Track completed steps
  const [completedSteps, setCompletedSteps] = useState(new Set());

  // Check if can navigate to a specific step
  const canNavigateToStep = useCallback((targetIndex) => {
    // Can always go backwards
    if (targetIndex < currentStepIndex) return true;
    
    // Can only go forward if current step is completed
    return completedSteps.has(currentStepIndex);
  }, [currentStepIndex, completedSteps]);

  // Navigate to specific step
  const goToStep = useCallback((stepIndex) => {
    if (stepIndex >= 0 && stepIndex < steps.length && canNavigateToStep(stepIndex)) {
      setIsNavigating(true);
      navigate(`${baseUrl}${steps[stepIndex].path}`);
      setIsNavigating(false);
    }
  }, [steps, navigate, baseUrl, canNavigateToStep]);

  // Navigation helpers
  const goToNext = useCallback(() => {
    if (currentStepIndex < steps.length - 1) {
      goToStep(currentStepIndex + 1);
    }
  }, [currentStepIndex, steps.length, goToStep]);

  const goToPrevious = useCallback(() => {
    if (currentStepIndex > 0) {
      goToStep(currentStepIndex - 1);
    }
  }, [currentStepIndex, goToStep]);

  // Mark current step as completed
  const markStepCompleted = useCallback((stepIndex = currentStepIndex) => {
    setCompletedSteps(prev => new Set([...prev, stepIndex]));
  }, [currentStepIndex]);

  // Mark step as incomplete
  const markStepIncomplete = useCallback((stepIndex = currentStepIndex) => {
    setCompletedSteps(prev => {
      const newSet = new Set(prev);
      newSet.delete(stepIndex);
      return newSet;
    });
  }, [currentStepIndex]);

  // Check if can proceed to next step
  const canProceed = useMemo(() => {
    return currentStepIndex < steps.length - 1 && completedSteps.has(currentStepIndex);
  }, [currentStepIndex, steps.length, completedSteps]);

  // Check if can go back
  const canGoBack = useMemo(() => {
    return currentStepIndex > 0;
  }, [currentStepIndex]);

  return {
    currentStep: steps[currentStepIndex],
    currentStepIndex,
    isFirstStep: currentStepIndex === 0,
    isLastStep: currentStepIndex === steps.length - 1,
    canProceed,
    canGoBack,
    goToNext,
    goToPrevious,
    goToStep,
    markStepCompleted,
    markStepIncomplete,
    completedSteps: Array.from(completedSteps),
    isNavigating,
  };
};

export default useNavigation;