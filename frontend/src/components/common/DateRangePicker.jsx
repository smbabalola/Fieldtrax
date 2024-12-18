// File: /frontend/src/components/common/DateRangePicker.jsx
import React from 'react';

const DateRangePicker = ({ startDate, endDate, onChange, className }) => {
  const handleStartDateChange = (e) => {
    onChange({
      startDate: e.target.value,
      endDate: endDate
    });
  };

  const handleEndDateChange = (e) => {
    onChange({
      startDate: startDate,
      endDate: e.target.value
    });
  };

  return (
    <div className={`d-flex gap-2 ${className}`}>
      <input
        type="date"
        className="form-control"
        value={startDate || ''}
        onChange={handleStartDateChange}
        placeholder="Start Date"
      />
      <input
        type="date"
        className="form-control"
        value={endDate || ''}
        onChange={handleEndDateChange}
        placeholder="End Date"
      />
    </div>
  );
};

export default DateRangePicker;