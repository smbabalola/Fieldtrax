// src/contexts/NavigationContext.jsx
import React, { createContext, useContext, useCallback } from 'react';
import PropTypes from 'prop-types';
import useNavigation from '../hooks/useNavigation';

const NavigationContext = createContext(null);

export const NavigationProvider = ({ 
  children, 
  steps, 
  baseUrl, 
  validationSchema,
  onStepChange 
}) => {
  const navigation = useNavigation(steps, baseUrl, validationSchema);

  // Handle step changes with validation
  const handleStepChange = useCallback(async (direction, currentData) => {
    if (onStepChange) {
      const canChange = await onStepChange(direction, navigation.currentStepIndex, currentData);
      if (!canChange) return;
    }

    if (direction === 'next') {
      navigation.goToNext();
    } else if (direction === 'previous') {
      navigation.goToPrevious();
    }
  }, [onStepChange, navigation]);

  const value = {
    ...navigation,
    handleStepChange,
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};

NavigationProvider.propTypes = {
  children: PropTypes.node.isRequired,
  steps: PropTypes.arrayOf(PropTypes.shape({
    path: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
  })).isRequired,
  baseUrl: PropTypes.string.isRequired,
  validationSchema: PropTypes.object,
  onStepChange: PropTypes.func,
};

export const useNavigationContext = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigationContext must be used within a NavigationProvider');
  }
  return context;
};

export default NavigationContext;