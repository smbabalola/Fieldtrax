import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import MainSidebar from './MainSidebar';
import JobSidebar from './JobSidebar';

const DualSidebarLayout = () => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="wrapper d-flex">
      {/* Main Sidebar */}
      <div className={`sidebar-wrapper ${collapsed ? 'collapsed' : ''}`}>
        <MainSidebar />
      </div>

      {/* Job Sidebar */}
      <div className={`job-sidebar-wrapper ${collapsed ? 'expanded' : ''}`}>
        <JobSidebar />
      </div>

      {/* Main Content */}
      <div className="main-content flex-grow-1 min-vh-100">
        <div className="content p-4">
          <Outlet />
        </div>
      </div>

      {/* Toggle Button */}
      <button
        className="sidebar-toggle btn btn-sm btn-light"
        onClick={() => setCollapsed(!collapsed)}
      >
        <i className={`bi bi-chevron-${collapsed ? 'right' : 'left'}`}></i>
      </button>

      <style jsx>{`
        .wrapper {
          min-height: 100vh;
          overflow-x: hidden;
        }

        .sidebar-wrapper {
          width: 250px;
          transition: all 0.3s ease;
        }

        .sidebar-wrapper.collapsed {
          width: 0;
          overflow: hidden;
        }

        .job-sidebar-wrapper {
          width: 300px;
          transition: all 0.3s ease;
        }

        .job-sidebar-wrapper.expanded {
          width: 350px;
        }

        .main-content {
          transition: all 0.3s ease;
        }

        .sidebar-toggle {
          position: fixed;
          left: 250px;
          top: 50%;
          transform: translateY(-50%);
          z-index: 1000;
          width: 24px;
          height: 48px;
          padding: 0;
          border-radius: 0 4px 4px 0;
          border: 1px solid #dee2e6;
          border-left: none;
          background: white;
          transition: all 0.3s ease;
        }

        .sidebar-toggle:hover {
          background: #f8f9fa;
        }

        .sidebar-wrapper.collapsed + .job-sidebar-wrapper .sidebar-toggle {
          left: 0;
        }
      `}</style>
    </div>
  );
};

export default DualSidebarLayout;