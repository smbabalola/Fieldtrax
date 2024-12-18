// File: /frontend/src/components/common/StatusBadge.jsx
import React from 'react';
import { Badge } from 'react-bootstrap';

export const StatusBadge = ({ status, type = 'default' }) => {
  const getVariant = () => {
    if (type === 'job') {
      switch (status?.toLowerCase()) {
        case 'active': return 'success';
        case 'planned': return 'primary';
        case 'completed': return 'info';
        case 'on hold': return 'warning';
        default: return 'secondary';
      }
    }
    return status?.toLowerCase() === 'active' ? 'success' : 'secondary';
  };

  return (
    <Badge bg={getVariant()} className="status-badge">
      {status}
    </Badge>
  );
};
