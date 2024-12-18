// File: /frontend/src/constants.js
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
    length: {
      units: ['ft', 'm', 'in', 'cm'],
      defaultDecimals: 2
    },
    pressure: {
      units: ['psi', 'bar', 'kpa', 'mpa'],
      defaultDecimals: 1
    },
    temperature: {
      units: ['f', 'c', 'k'],
      defaultDecimals: 1
    },
    weight: {
      units: ['lbs', 'kg', 'g'],
      defaultDecimals: 1
    },
    volume: {
      units: ['bbl', 'm3', 'gal', 'l'],
      defaultDecimals: 1
    },
    density: {
      units: ['ppg', 'kg/m3', 'g/cm3'],
      defaultDecimals: 2
    },
    torque: {
      units: ['ft-lbs', 'nm'],
      defaultDecimals: 0
    },
    rotation: {
      units: ['rpm'],
      defaultDecimals: 0
    }
  };
  
  export const DEFAULT_SETTINGS = {
    unitSystem: 'US',
    unitPreferences: REGION_PRESETS.US,
    displaySettings: {
      decimalPlaces: {
        length: 2,
        pressure: 1,
        temperature: 1,
        weight: 1,
        volume: 1,
        density: 2,
        torque: 0,
        rotation: 0
      },
      fontSize: 'medium',
      darkMode: false,
      highContrast: false
    }
  };
  
  export const DISPLAY_OPTIONS = {
    fontSizes: [
      { value: 'small', label: 'Small' },
      { value: 'medium', label: 'Medium' },
      { value: 'large', label: 'Large' }
    ],
    themeOptions: [
      { value: 'darkMode', label: 'Dark Mode' },
      { value: 'highContrast', label: 'High Contrast' }
    ]
  };
  
  export const API_ENDPOINTS = {
    settings: '/api/v1/settings',
    auth: '/api/v1/auth',
    jobs: '/api/v1/jobs'
  };
  
  export const ROUTES = {
    dashboard: '/dashboard',
    settings: '/settings',
    jobs: '/jobs',
    rigs: '/rigs',
    reports: '/reports',
    login: '/login',
    forgotPassword: '/forgot-password'
  };
  
  // Default values for mock/preview data
  export const SAMPLE_VALUES = {
    length: 100.0,
    pressure: 2000.0,
    temperature: 75.0,
    weight: 5000.0,
    volume: 50.0,
    density: 8.6,
    torque: 1000.0,
    rotation: 120.0
  };
  
  // Layout constants
  export const LAYOUT = {
    mainSidebarWidth: 240,
    jobSidebarWidth: 200,
    collapsedSidebarWidth: 60,
    headerHeight: 56,
    footerHeight: 40
  };