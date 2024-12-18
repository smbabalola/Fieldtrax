import React from 'react';

const LoadingSpinner = ({
  fullHeight = false,
  text = 'Loading FieldTrax',
  size = 'regular',
  showText = true,
  className = ''
}) => {
  const containerClasses = `d-flex align-items-center justify-content-center ${
    fullHeight ? 'min-vh-100' : ''
  } ${className}`;

  const spinnerSizeClass = size === 'small' ? '' : 'mb-3';
  const spinnerClass = `spinner-border text-primary ${spinnerSizeClass}`;
  const textClass = size === 'small' ? 'h6' : 'h4';

  return (
    <div className={containerClasses}>
      <div className="text-center">
        <div className={spinnerClass} role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        {showText && <h4 className={`text-primary ${textClass}`}>{text}</h4>}
      </div>
    </div>
  );
};

export default LoadingSpinner;