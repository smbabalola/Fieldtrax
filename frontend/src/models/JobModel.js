// src/models/JobModel.js
export const initialJobFormData = {
    // Customer Information
    operator_id: '',
    contract_id: '',
    po_number: '',
    po_amount: '',
    po_start_date: '',
    po_end_date: '',
    
    // Well Information
    well_id: '',
    field_name: '',
    well_type: '',
    well_status: '',
    spud_date: '',
    total_depth_planned: '',
    
    // Rig Information
    rig_id: '',
    rig_type: '',
    rig_capability: '',
    rig_status: '',
    
    // Wellbore Geometry
    wellbore_type: '',
    total_depth: '',
    casing_design: [],
    liner_design: [],
    
    // Trajectory
    trajectory_type: '',
    kickoff_depth: '',
    target_depth: '',
    survey_data: [],
    
    // Fluids
    primary_fluid_type: '',
    fluid_properties: {
      density: '',
      viscosity: '',
      ph: '',
    },
    fluid_volumes: [],
  };
  
  export const jobValidationRules = {
    // Customer Information
    operator_id: {
      required: true,
      message: 'Operator is required'
    },
    contract_id: {
      required: true,
      message: 'Contract is required'
    },
    po_number: {
      required: true,
      message: 'PO Number is required'
    },
    
    // Well Information
    well_id: {
      required: true,
      message: 'Well is required'
    },
    field_name: {
      required: true,
      message: 'Field name is required'
    },
    well_type: {
      required: true,
      message: 'Well type is required'
    },
    
    // Rig Information
    rig_id: {
      required: true,
      message: 'Rig is required'
    },
    rig_type: {
      required: true,
      message: 'Rig type is required'
    },
    
    // Wellbore Geometry
    wellbore_type: {
      required: true,
      message: 'Wellbore type is required'
    },
    total_depth: {
      required: true,
      message: 'Total depth is required',
      type: 'number',
      min: 0
    },
    
    // Trajectory
    trajectory_type: {
      required: true,
      message: 'Trajectory type is required'
    },
    
    // Fluids
    primary_fluid_type: {
      required: true,
      message: 'Primary fluid type is required'
    }
  };
  
  export const validateJobForm = (formData) => {
    const errors = {};
    
    Object.entries(jobValidationRules).forEach(([field, rules]) => {
      const value = formData[field];
      
      if (rules.required && (!value || value === '')) {
        errors[field] = rules.message;
      }
      
      if (rules.type === 'number' && value) {
        const numValue = Number(value);
        if (isNaN(numValue)) {
          errors[field] = 'Must be a number';
        } else if (rules.min !== undefined && numValue < rules.min) {
          errors[field] = `Must be greater than ${rules.min}`;
        }
      }
    });
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };