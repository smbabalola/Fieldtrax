 // src/utils/validation.js
 export const validateJobData = (jobData) => {
    const errors = {};
  
    if (!jobData.jobcenter_id) errors.jobcenter_id = 'Job Center is required';
    if (!jobData.rig_id) errors.rig_id = 'Rig is required';
    if (!jobData.operator_id) errors.operator_id = 'Operator is required';
    if (!jobData.well_id) errors.well_id = 'Well ID is required';
    if (!jobData.country) errors.country = 'Country is required';
    if (!jobData.field) errors.field = 'Field is required';
    if (!jobData.spud_date) errors.spud_date = 'Spud Date is required';
  
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };