// File: /frontend/src/layouts/JobLayout.jsx
import React from 'react';
import { Outlet, useParams } from 'react-router-dom';
import JobSidebar from './JobSidebar';

const JobLayout = () => {
  const { jobId } = useParams();

  return (
    <div className="d-flex h-100">
      {/* Job Navigation Sidebar */}
      <JobSidebar jobId={jobId} />

      {/* Job Content Area */}
      <div className="flex-grow-1 p-4">
        <Outlet />
      </div>
    </div>
  );
};

export default JobLayout;



