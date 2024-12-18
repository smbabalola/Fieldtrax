// File: src/utils/settingsValidation.js

// Validate number format settings
const validateNumberFormat = (settings) => {
    const errors = {};
  
    if (settings.useSignificantDigits) {
      const sigDigits = parseInt(settings.significantDigits);
      if (isNaN(sigDigits) || sigDigits < 1 || sigDigits > 10) {
        errors.significantDigits = 'Significant digits must be between 1 and 10';
      }
    }
  
    return errors;
  };
  
  // Validate unit settings
  const validateUnitSettings = (units) => {
    const errors = {};
    const requiredUnits = [
      'lengthUnit',
      'pressureUnit',
      'temperatureUnit',
      'weightUnit',
      'volumeUnit',
      'densityUnit',
      'torqueUnit'
    ];
  
    requiredUnits.forEach(unit => {
      if (!units[unit]) {
        errors[unit] = `${unit.replace('Unit', '')} unit is required`;
      }
    });
  
    return errors;
  };
  
  // Validate decimal places
  const validateDecimalPlaces = (settings) => {
    const errors = {};
    const decimalPlaces = settings.decimalPlaces || {};
  
    Object.entries(decimalPlaces).forEach(([key, value]) => {
      const numValue = parseInt(value);
      if (isNaN(numValue) || numValue < 0 || numValue > 10) {
        errors[`${key}Decimals`] = `${key} decimal places must be between 0 and 10`;
      }
    });
  
    return errors;
  };
  
  // Validate display settings
  const validateDisplaySettings = (settings) => {
    const errors = {};
  
    if (settings.fontSize && !['small', 'medium', 'large'].includes(settings.fontSize)) {
      errors.fontSize = 'Invalid font size selection';
    }
  
    if (settings.unitFormat?.position && !['before', 'after'].includes(settings.unitFormat.position)) {
      errors.unitPosition = 'Invalid unit position';
    }
  
    return errors;
  };
  
  // Main validation function
  export const validateSettings = (settings) => {
    return {
      ...validateUnitSettings(settings),
      ...validateNumberFormat(settings.numberFormat || {}),
      ...validateDecimalPlaces(settings),
      ...validateDisplaySettings(settings)
    };
  };
  
  // Helper function to check if settings are valid
  export const isValidSettings = (settings) => {
    const errors = validateSettings(settings);
    return Object.keys(errors).length === 0;
  };
  
  // Helper function to get default values for invalid settings
  export const getDefaultValueForSetting = (settingName) => {
    const defaults = {
      lengthUnit: 'ft',
      pressureUnit: 'psi',
      temperatureUnit: 'f',
      weightUnit: 'lbs',
      volumeUnit: 'bbl',
      densityUnit: 'ppg',
      torqueUnit: 'ft-lbs',
      fontSize: 'medium',
      decimalPlaces: {
        length: 2,
        pressure: 1,
        temperature: 1,
        weight: 1,
        volume: 1,
        density: 2,
        torque: 0
      }
    };
  
    return defaults[settingName];
  };
  
  // Validate individual setting
  export const validateSetting = (settingName, value) => {
    const tempSettings = {
      [settingName]: value
    };
    
    const errors = validateSettings(tempSettings);
    return errors[settingName];
  };
  
  // Format validation error messages
  export const formatValidationError = (error) => {
    if (typeof error === 'string') return error;
    
    if (Array.isArray(error)) {
      return error.join(', ');
    }
    
    if (typeof error === 'object') {
      return Object.values(error).join(', ');
    }
    
    return 'Invalid value';
  };