// File: /frontend/src/components/common/ModuleHeader.jsx
import React from 'react';

export const ModuleHeader = ({ title, subtitle, actions }) => {
  return (
    <div className="module-header">
      <div>
        <h4 className="module-title">{title}</h4>
        {subtitle && <div className="text-muted">{subtitle}</div>}
      </div>
      {actions && <div className="module-actions">{actions}</div>}
    </div>
  );
};
export default ModuleHeader