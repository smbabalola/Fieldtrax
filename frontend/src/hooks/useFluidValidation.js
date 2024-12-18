// File: /frontend/src/hooks/useFluidValidation.js
import { useState, useCallback } from 'react';

export const useFluidValidation = (initialErrors = {}) => {
  const [errors, setErrors] = useState(initialErrors);

  const validateFluid = useCallback((fluidData) => {
    const newErrors = {};

    // Required fields
    if (!fluidData.type) {
      newErrors.type = 'Fluid type is required';
    }

    if (!fluidData.volume) {
      newErrors.volume = 'Volume is required';
    } else if (isNaN(fluidData.volume) || fluidData.volume <= 0) {
      newErrors.volume = 'Volume must be a positive number';
    }

    if (!fluidData.density) {
      newErrors.density = 'Density is required';
    } else if (isNaN(fluidData.density) || fluidData.density <= 0) {
      newErrors.density = 'Density must be a positive number';
    }

    // Optional fields validation
    if (fluidData.viscosity && (isNaN(fluidData.viscosity) || fluidData.viscosity < 0)) {
      newErrors.viscosity = 'Viscosity must be a non-negative number';
    }

    if (fluidData.ph && (isNaN(fluidData.ph) || fluidData.ph < 0 || fluidData.ph > 14)) {
      newErrors.ph = 'pH must be between 0 and 14';
    }

    if (fluidData.chlorides && (isNaN(fluidData.chlorides) || fluidData.chlorides < 0)) {
      newErrors.chlorides = 'Chlorides must be a non-negative number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, []);

  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  const setFieldError = useCallback((field, error) => {
    setErrors(prev => ({
      ...prev,
      [field]: error
    }));
  }, []);

  return {
    errors,
    validateFluid,
    clearErrors,
    setFieldError,
    hasErrors: Object.keys(errors).length > 0
  };
};

// Validation Rules
export const FLUID_VALIDATION_RULES = {
  type: {
    required: true,
    message: 'Fluid type is required'
  },
  volume: {
    required: true,
    type: 'number',
    min: 0,
    message: 'Volume must be a positive number'
  },
  density: {
    required: true,
    type: 'number',
    min: 0,
    message: 'Density must be a positive number'
  },
  viscosity: {
    type: 'number',
    min: 0,
    message: 'Viscosity must be a non-negative number'
  },
  ph: {
    type: 'number',
    min: 0,
    max: 14,
    message: 'pH must be between 0 and 14'
  },
  chlorides: {
    type: 'number',
    min: 0,
    message: 'Chlorides must be a non-negative number'
  }
};