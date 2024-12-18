// File: /frontend/src/components/common/StatCard.jsx
import React from 'react';
import { Card } from 'react-bootstrap';

export const StatCard = ({ title, value, icon }) => {
  return (
    <Card className="stat-card">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <div className="stat-value">{value}</div>
            <div className="stat-label">{title}</div>
          </div>
          {icon && <div className="stat-icon text-primary">{icon}</div>}
        </div>
      </Card.Body>
    </Card>
  );
};