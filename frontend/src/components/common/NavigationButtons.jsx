// src/components/common/NavigationButtons.jsx
import React from 'react';
import { Button } from 'react-bootstrap';
import PropTypes from 'prop-types';

const NavigationButtons = ({ 
  onPrevious,
  onNext,
  onSave,
  canGoNext = true,
  canGoPrevious = true,
  canSave = true,
  showSave = true,
  isLastStep = false,
  isLoading = false 
}) => {
  return (
    <div className="d-flex justify-content-between mt-4 mb-3">
      <Button
        variant="outline-secondary"
        onClick={onPrevious}
        disabled={!canGoPrevious || isLoading}
      >
        <i className="bi bi-arrow-left me-2"></i>
        Previous
      </Button>

      <div className="d-flex gap-2">
        {showSave && (
          <Button
            variant="success"
            onClick={onSave}
            disabled={!canSave || isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Saving...
              </>
            ) : (
              <>
                <i className="bi bi-check-circle me-2"></i>
                Save
              </>
            )}
          </Button>
        )}
        
        {!isLastStep && (
          <Button
            variant="primary"
            onClick={onNext}
            disabled={!canGoNext || isLoading}
          >
            Next
            <i className="bi bi-arrow-right ms-2"></i>
          </Button>
        )}
      </div>
    </div>
  );
};

NavigationButtons.propTypes = {
  onPrevious: PropTypes.func.isRequired,
  onNext: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  canGoNext: PropTypes.bool,
  canGoPrevious: PropTypes.bool,
  canSave: PropTypes.bool,
  showSave: PropTypes.bool,
  isLastStep: PropTypes.bool,
  isLoading: PropTypes.bool
};

export default NavigationButtons;