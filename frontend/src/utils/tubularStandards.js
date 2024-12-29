// File: /src/utils/tubularStandards.js

// API Casing Grades
export const standardGrades = [
    'H40',
    'J55',
    'K55',
    'N80',
    'L80',
    'C90',
    'C95',
    'T95',
    'P110',
    'Q125',
    'V150'
];

// Common Thread Types
export const standardThreads = [
    'BTC', // Buttress Thread Casing
    'LTC', // Long Thread Casing
    'STC', // Short Thread Casing
    'Premium',
    'VAM TOP',
    'VAM 21',
    'TenarisHydril',
    'FOX',
    'BEAR',
    'ER',    // External Upset Round
    'IF',    // Internal Flush
    'NH',    // Numbered Hub
    'REG',   // Regular
    'XL'     // Extra Long
];

// Common Casing Sizes (OD in inches)
export const standardCasingSizes = [
    30,     // Conductor Casing
    20,     // Surface Casing
    16,
    13.375, // Intermediate Casing
    11.75,
    9.625,  // Production Casing
    7.625,
    7,      // Production Liner
    5.5,
    4.5     // Production Tubing
];

// API Steel Grades Properties
export const gradeProperties = {
    'H40': {
        minYieldStrength: 40000, // psi
        maxYieldStrength: 80000,
        minTensileStrength: 60000
    },
    'J55': {
        minYieldStrength: 55000,
        maxYieldStrength: 80000,
        minTensileStrength: 75000
    },
    'K55': {
        minYieldStrength: 55000,
        maxYieldStrength: 80000,
        minTensileStrength: 95000
    },
    'N80': {
        minYieldStrength: 80000,
        maxYieldStrength: 110000,
        minTensileStrength: 100000
    },
    'L80': {
        minYieldStrength: 80000,
        maxYieldStrength: 95000,
        minTensileStrength: 95000
    },
    'C90': {
        minYieldStrength: 90000,
        maxYieldStrength: 105000,
        minTensileStrength: 100000
    },
    'C95': {
        minYieldStrength: 95000,
        maxYieldStrength: 110000,
        minTensileStrength: 105000
    },
    'T95': {
        minYieldStrength: 95000,
        maxYieldStrength: 110000,
        minTensileStrength: 105000
    },
    'P110': {
        minYieldStrength: 110000,
        maxYieldStrength: 140000,
        minTensileStrength: 125000
    },
    'Q125': {
        minYieldStrength: 125000,
        maxYieldStrength: 150000,
        minTensileStrength: 135000
    },
    'V150': {
        minYieldStrength: 150000,
        maxYieldStrength: 170000,
        minTensileStrength: 160000
    }
};

// Utility Functions for Tubular Calculations
export const calculateBurst = (od, id, grade, wallFactor = 0.875) => {
    const wallThickness = (od - id) / 2;
    const yieldStrength = gradeProperties[grade]?.minYieldStrength || 0;
    return 2 * wallThickness * yieldStrength * wallFactor / od;
};

export const calculateCollapse = (od, id, grade) => {
    const wallThickness = (od - id) / 2;
    const ratio = od / wallThickness;
    const yieldStrength = gradeProperties[grade]?.minYieldStrength || 0;
    
    // Simplified collapse calculation - actual calculation would need more complex formulas
    return (46.95 * Math.pow(10, 6)) / Math.pow(ratio, 2.73);
};

export const calculateDrift = (id, tolerance = 0.125) => {
    return id - tolerance;
};

export const validateTubular = (tubularData) => {
    const errors = [];
    
    if (tubularData.outer_diameter <= tubularData.inner_diameter) {
        errors.push('Outer diameter must be greater than inner diameter');
    }
    
    if (!standardGrades.includes(tubularData.grade)) {
        errors.push('Invalid grade selected');
    }
    
    if (!standardThreads.includes(tubularData.thread)) {
        errors.push('Invalid thread type selected');
    }
    
    if (tubularData.start_depth >= tubularData.end_depth) {
        errors.push('End depth must be greater than start depth');
    }
    
    return errors;
};

// Drift Diameter Calculator based on API specifications
export const calculateAPIStandardDrift = (nominalSize) => {
    const driftTable = {
        '4.5': 3.875,
        '5.5': 4.653,
        '7': 5.969,
        '7.625': 6.500,
        '9.625': 8.500,
        '11.75': 10.625,
        '13.375': 12.250,
        '16': 14.875,
        '20': 18.875,
        '30': 28.500
    };
    
    return driftTable[nominalSize.toString()] || null;
};

export default {
    standardGrades,
    standardThreads,
    standardCasingSizes,
    gradeProperties,
    calculateBurst,
    calculateCollapse,
    calculateDrift,
    validateTubular,
    calculateAPIStandardDrift
};