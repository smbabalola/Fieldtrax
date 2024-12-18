// File: src/utils/unitConversion.js

// Conversion factors
const CONVERSION_FACTORS = {
    length: {
      ft: 1,
      m: 0.3048,
      in: 12
    },
    pressure: {
      psi: 1,
      bar: 0.0689476,
      kPa: 6.89476,
      MPa: 0.00689476
    },
    temperature: {
      f: value => value,
      c: value => (value - 32) * (5/9)
    },
    weight: {
      lbs: 1,
      kg: 0.453592,
      klbs: 0.001
    },
    volume: {
      bbl: 1,
      m3: 0.158987,
      gal: 42
    },
    density: {
      ppg: 1,
      'kg/m3': 119.826427,
      sg: 0.120048
    },
    torque: {
      'ft-lbs': 1,
      'n-m': 1.35582,
      'kg-m': 0.138255
    }
  };
  
  // Convert value between units
  export const convertUnit = (value, fromUnit, toUnit, type) => {
    if (fromUnit === toUnit) return value;
    
    const factors = CONVERSION_FACTORS[type];
    if (!factors) throw new Error(`Unknown unit type: ${type}`);
  
    if (type === 'temperature') {
      // Special case for temperature
      const celsius = fromUnit === 'f' ? factors.c(value) : value;
      return toUnit === 'f' ? (celsius * 9/5) + 32 : celsius;
    }
  
    // Standard conversion
    const baseValue = value / factors[fromUnit];
    return baseValue * factors[toUnit];
  };
  
  // Format value according to settings
  export const formatValue = (value, unit, type, decimalPlaces) => {
    const formatted = Number(value).toFixed(decimalPlaces);
    return `${formatted} ${unit}`;
  };
  
  // Convert and format value
  export const convertAndFormat = (value, fromUnit, toUnit, type, decimalPlaces) => {
    const converted = convertUnit(value, fromUnit, toUnit, type);
    return formatValue(converted, toUnit, type, decimalPlaces);
  };
  
  // Batch convert multiple values
  export const batchConvert = (values, fromUnit, toUnit, type) => {
    return values.map(value => convertUnit(value, fromUnit, toUnit, type));
  };
  
  // Get available units for a type
  export const getAvailableUnits = (type) => {
    return Object.keys(CONVERSION_FACTORS[type] || {});
  };
  
  // Validate if a unit is valid for a type
  export const isValidUnit = (unit, type) => {
    return getAvailableUnits(type).includes(unit);
  };
  
  // Get default unit for a type based on region
  export const getDefaultUnit = (type, region = 'US') => {
    const defaults = {
      US: {
        length: 'ft',
        pressure: 'psi',
        temperature: 'f',
        weight: 'lbs',
        volume: 'bbl',
        density: 'ppg',
        torque: 'ft-lbs'
      },
      METRIC: {
        length: 'm',
        pressure: 'bar',
        temperature: 'c',
        weight: 'kg',
        volume: 'm3',
        density: 'kg/m3',
        torque: 'n-m'
      }
    };
    
    return defaults[region]?.[type];
  };
  
  // Helper function to round to significant digits
  export const roundToSignificant = (value, digits) => {
    if (value === 0) return 0;
    const magnitude = Math.floor(Math.log10(Math.abs(value)));
    const factor = Math.pow(10, digits - magnitude - 1);
    return Math.round(value * factor) / factor;
  };
  
  // Format large numbers with appropriate units (k, M, etc.)
  export const formatLargeNumber = (value, decimalPlaces = 1) => {
    const units = ['', 'k', 'M', 'G'];
    let unitIndex = 0;
    let scaledValue = value;
  
    while (scaledValue >= 1000 && unitIndex < units.length - 1) {
      unitIndex += 1;
      scaledValue /= 1000;
    }
  
    return `${scaledValue.toFixed(decimalPlaces)}${units[unitIndex]}`;
  };