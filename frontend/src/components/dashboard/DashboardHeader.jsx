// src/components/dashboard/DashboardHeader.jsx
import React from 'react';
import { Container, Button } from 'react-bootstrap';
import { Search, Plus } from 'react-bootstrap-icons';

const DashboardHeader = ({ 
  activeTab, 
  setActiveTab, 
  searchTerm, 
  setSearchTerm, 
  onCreateNew 
}) => {
  return (
    <div className="border-bottom bg-white sticky-top">
      <Container fluid className="py-3">
        <div className="d-flex justify-content-between align-items-center">
          <div className="d-flex gap-4 align-items-center">
            <h4 className="mb-0">Dashboard</h4>
            <div className="d-flex gap-3">
              <Button 
                variant={activeTab === 'overview' ? 'primary' : 'link'} 
                className="text-decoration-none"
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </Button>
              <Button 
                variant={activeTab === 'analytics' ? 'primary' : 'link'}
                className="text-decoration-none"
                onClick={() => setActiveTab('analytics')}
              >
                Analytics
              </Button>
            </div>
          </div>
          <div className="d-flex gap-2">
            <div className="position-relative">
              <input
                type="text"
                className="form-control"
                placeholder="Search jobs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ paddingLeft: '2.5rem' }}
              />
              <Search 
                className="position-absolute"
                style={{ left: '0.75rem', top: '50%', transform: 'translateY(-50%)' }}
              />
            </div>
            <Button onClick={onCreateNew}>
              <Plus className="me-2" />
              New Job
            </Button>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default DashboardHeader;