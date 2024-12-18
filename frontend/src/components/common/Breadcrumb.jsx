// src/components/common/Breadcrumb.jsx
import React from 'react';
import { Breadcrumb as BSBreadcrumb } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight } from 'react-bootstrap-icons';

const Breadcrumb = () => {
  const location = useLocation();
  const paths = location.pathname.split('/').filter(path => path);

  // Map path segments to readable names
  const getPathName = (path) => {
    const pathMap = {
      rigs: 'Rigs',
      settings: 'Settings',
      job: 'Job',
      'physical-barriers': 'Physical Barriers',
      fluid: 'Fluid',
      'delivery-tickets': 'Delivery Tickets',
      tally: 'Tally',
      'job-logs': 'Job Logs',
      'service-tickets': 'Service Tickets',
      backload: 'Backload',
      'client-feedback': 'Client Feedback'
    };

    return pathMap[path] || path;
  };

  return (
    <BSBreadcrumb className="bg-transparent px-0 py-2 mb-4">
      <BSBreadcrumb.Item 
        linkAs={Link} 
        linkProps={{ to: '/' }}
        className="text-decoration-none"
      >
        Home
      </BSBreadcrumb.Item>
      {paths.map((path, index) => {
        const isLast = index === paths.length - 1;
        const to = `/${paths.slice(0, index + 1).join('/')}`;
        
        return (
          <BSBreadcrumb.Item
            key={path}
            active={isLast}
            linkAs={!isLast ? Link : undefined}
            linkProps={!isLast ? { to } : undefined}
            className="text-decoration-none"
          >
            {getPathName(path)}
          </BSBreadcrumb.Item>
        );
      })}
    </BSBreadcrumb>
  );
};

export default Breadcrumb;