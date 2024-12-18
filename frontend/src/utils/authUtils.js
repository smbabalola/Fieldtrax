// File: /frontend/src/utils/authUtils.js
import { useSelector } from 'react-redux';

// Permission constants
export const PERMISSIONS = {
  JOBS: {
    VIEW: 'jobs:view',
    CREATE: 'jobs:create',
    EDIT: 'jobs:edit',
    DELETE: 'jobs:delete'
  },
  WELLS: {
    VIEW: 'wells:view',
    CREATE: 'wells:create',
    EDIT: 'wells:edit'
  },
  FLUIDS: {
    VIEW: 'fluids:view',
    CREATE: 'fluids:create',
    EDIT: 'fluids:edit'
  },
  BARRIERS: {
    VIEW: 'barriers:view',
    CREATE: 'barriers:create',
    EDIT: 'barriers:edit'
  },
  PURCHASE_ORDERS: {
    VIEW: 'purchase_orders:view',
    CREATE: 'purchase_orders:create',
    APPROVE: 'purchase_orders:approve'
  }
};

// Custom hook for handling permissions
export const usePermissions = () => {
  const { user } = useSelector(state => state.auth);
  
  const hasPermission = (permission) => {
    if (!user?.permissions) return false;
    if (user.role === 'admin') return true;
    return user.permissions.includes(permission);
  };

  const checkMultiplePermissions = (permissions) => {
    return permissions.every(permission => hasPermission(permission));
  };

  return {
    hasPermission,
    checkMultiplePermissions,
    isAdmin: user?.role === 'admin'
  };
};

// Permission-based component wrapper
export const WithPermission = ({ permission, children, fallback = null }) => {
  const { hasPermission } = usePermissions();
  return hasPermission(permission) ? children : fallback;
};