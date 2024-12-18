// File: /frontend/src/constants/index.js
export const REGION_PRESETS = {
    US: {
      lengthUnit: 'ft',
      pressureUnit: 'psi',
      temperatureUnit: 'f',
      weightUnit: 'lbs',
      volumeUnit: 'bbl',
      densityUnit: 'ppg',
      torqueUnit: 'ft-lbs',
      rotationUnit: 'rpm'
    },
    METRIC: {
      lengthUnit: 'm',
      pressureUnit: 'bar',
      temperatureUnit: 'c',
      weightUnit: 'kg',
      volumeUnit: 'm3',
      densityUnit: 'kg/m3',
      torqueUnit: 'nm',
      rotationUnit: 'rpm'
    }
  };
  
  export const UNIT_TYPES = {
    length: ['ft', 'm', 'in', 'cm'],
    pressure: ['psi', 'bar', 'kpa', 'mpa'],
    temperature: ['f', 'c', 'k'],
    weight: ['lbs', 'kg', 'g'],
    volume: ['bbl', 'm3', 'gal', 'l'],
    density: ['ppg', 'kg/m3', 'g/cm3'],
    torque: ['ft-lbs', 'nm'],
    rotation: ['rpm']
  };