import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Nav } from 'react-bootstrap';

const MainSidebar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="sidebar bg-light border-end">
      <div className="sidebar-header p-3 border-bottom">
        <h5 className="mb-0">FieldTrax</h5>
      </div>
      <Nav className="flex-column p-3">
        <Nav.Item>
          <Link
            to="/dashboard"
            className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
          >
            <i className="bi bi-speedometer2 me-2"></i>
            Dashboard
          </Link>
        </Nav.Item>
        <Nav.Item>
          <Link
            to="/jobs"
            className={`nav-link ${isActive('/jobs') ? 'active' : ''}`}
          >
            <i className="bi bi-briefcase me-2"></i>
            Jobs
          </Link>
        </Nav.Item>
        <Nav.Item>
          <Link
            to="/rigs"
            className={`nav-link ${isActive('/rigs') ? 'active' : ''}`}
          >
            <i className="bi bi-gear me-2"></i>
            Rigs
          </Link>
        </Nav.Item>
        <Nav.Item>
          <Link
            to="/reports"
            className={`nav-link ${isActive('/reports') ? 'active' : ''}`}
          >
            <i className="bi bi-file-text me-2"></i>
            Reports
          </Link>
        </Nav.Item>
        <Nav.Item>
          <Link
            to="/settings"
            className={`nav-link ${isActive('/settings') ? 'active' : ''}`}
          >
            <i className="bi bi-sliders me-2"></i>
            Settings
          </Link>
        </Nav.Item>
      </Nav>
    </div>
  );
};

export default MainSidebar;