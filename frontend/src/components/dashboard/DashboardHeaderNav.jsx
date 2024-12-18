// src/components/dashboard/DashboardHeaderNav.jsx
import React from 'react';
import { Nav } from 'react-bootstrap';
import { useLocation, Link } from 'react-router-dom';

const DashboardHeaderNav = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  const headerTabs = [
    { path: '/overview', label: 'Overview-Job details' },
    { path: '/well', label: 'Well' },
    { path: '/purchase-order', label: 'Purchase Order' },
    { path: '/physical-barriers', label: 'Physical Barriers' },
    { path: '/fluid', label: 'Fluid' },
    { path: '/delivery-tickets', label: 'Delivery Tickets' },
    { path: '/tally', label: 'Tally' },
    { path: '/job-logs', label: 'Job Logs' },
    { path: '/service-tickets', label: 'Service Tickets' },
    { path: '/backload', label: 'Backload' },
    { path: '/client-feedback', label: 'Client Feedback' }
  ];

  return (
    <div className="bg-white border-bottom">
      <Nav 
        variant="tabs" 
        className="px-3 flex-nowrap overflow-auto"
        style={{ whiteSpace: 'nowrap' }}
      >
        {headerTabs.map((tab) => (
          <Nav.Item key={tab.path}>
            <Nav.Link
              as={Link}
              to={tab.path}
              active={currentPath.includes(tab.path)}
              className="border-0"
            >
              {tab.label}
            </Nav.Link>
          </Nav.Item>
        ))}
      </Nav>
    </div>
  );
};

export default DashboardHeaderNav;
