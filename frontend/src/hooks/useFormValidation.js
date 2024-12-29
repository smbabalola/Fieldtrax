// src/hooks/useFormValidation.js
import { useState, useCallback, useEffect } from 'react';
import { useDispatch } from 'react-redux';

const useFormValidation = (initialData = {}, validationSchema = {}, onValidationChange) => {
  const [formData, setFormData] = useState(initialData);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const dispatch = useDispatch();

  // Validate a single field
  const validateField = useCallback((name, value) => {
    if (!validationSchema[name]) return '';

    const rules = validationSchema[name];
    
    if (rules.required && (!value || value === '')) {
      return rules.message || 'This field is required';
    }

    if (rules.pattern && !rules.pattern.test(value)) {
      return rules.patternMessage || 'Invalid format';
    }

    if (rules.custom) {
      return rules.custom(value, formData);
    }

    return '';
  }, [validationSchema, formData]);

  // Validate all fields
  const validateForm = useCallback(() => {
    const newErrors = {};
    Object.keys(validationSchema).forEach(field => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
      }
    });
    return newErrors;
  }, [validateField, formData, validationSchema]);

  // Handle field change
  const handleChange = useCallback((event) => {
    const { name, value } = event.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  }, []);

  // Handle field blur
  const handleBlur = useCallback((event) => {
    const { name } = event.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  }, []);

  // Handle form submission
  const handleSubmit = useCallback(async (submitCallback) => {
    setIsSubmitting(true);
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length === 0) {
      try {
        await submitCallback(formData);
      } catch (error) {
        setErrors({ submit: error.message });
      }
    } else {
      setErrors(newErrors);
      setTouched(Object.keys(newErrors).reduce((acc, key) => ({
        ...acc,
        [key]: true
      }), {}));
    }
    setIsSubmitting(false);
  }, [formData, validateForm]);

  // Update errors whenever form data changes
  useEffect(() => {
    const newErrors = validateForm();
    setErrors(newErrors);
    if (onValidationChange) {
      onValidationChange(Object.keys(newErrors).length === 0);
    }
  }, [formData, validateForm, onValidationChange]);

  // Reset form
  const resetForm = useCallback(() => {
    setFormData(initialData);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialData]);

  // Set form data from external source
  const setExternalData = useCallback((data) => {
    setFormData(data);
  }, []);

  return {
    formData,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    resetForm,
    setExternalData,
    validateField,
    validateForm
  };
};

export default useFormValidation;