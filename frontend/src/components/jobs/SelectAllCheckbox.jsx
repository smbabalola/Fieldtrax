// File: /frontend/src/components/jobs/SelectAllCheckbox.jsx
import React, { useRef, useEffect } from 'react';

const SelectAllCheckbox = ({ jobs, selectedJobs, onChange }) => {
  const checkboxRef = useRef(null);
  const isChecked = selectedJobs.length === jobs.length && jobs.length > 0;
  const isIndeterminate = selectedJobs.length > 0 && selectedJobs.length < jobs.length;

  useEffect(() => {
    if (checkboxRef.current) {
      checkboxRef.current.indeterminate = isIndeterminate;
    }
  }, [isIndeterminate]);

  return (
    <input
      ref={checkboxRef}
      type="checkbox"
      onChange={onChange}
      checked={isChecked}
    />
  );
};

export default SelectAllCheckbox;