// File: /frontend/src/layouts/Sidebar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = ({ isOpen, onToggle }) => {
  return (
    <div className={`sidebar bg-dark text-white ${isOpen ? 'open' : 'closed'}`} 
         style={{ 
           width: isOpen ? '250px' : '60px',
           minHeight: '100vh',
           transition: 'width 0.3s ease'
         }}>
      <div className="p-3">
        <div className="d-flex justify-content-between align-items-center mb-4">
          {isOpen && <span className="fs-4">Menu</span>}
          <button 
            className="btn btn-link text-white p-0" 
            onClick={onToggle}
          >
            <i className="bi bi-list fs-4"></i>
          </button>
        </div>

        <nav className="nav flex-column">
          <Link to="/dashboard" className="nav-link text-white">
            <i className="bi bi-speedometer2 me-2"></i>
            {isOpen && 'Dashboard'}
          </Link>
          <Link to="/jobs" className="nav-link text-white">
            <i className="bi bi-briefcase me-2"></i>
            {isOpen && 'Jobs'}
          </Link>
          <Link to="/wells" className="nav-link text-white">
            <i className="bi bi-gear me-2"></i>
            {isOpen && 'Wells'}
          </Link>
          <Link to="/reports" className="nav-link text-white">
            <i className="bi bi-file-text me-2"></i>
            {isOpen && 'Reports'}
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;

