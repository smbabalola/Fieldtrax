// File: /frontend/src/routes/AppRouter.jsx
import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import DashboardLayout from '../layouts/DashboardLayout';
import JobsPage from '../pages/job/JobsPage';
import JobDetailsPage from '../pages/job/JobDetailsPage';
import JobForm from '../pages/job/JobForm';
import ProtectedRoute from './ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <ProtectedRoute><DashboardLayout /></ProtectedRoute>,
    children: [
      {
        path: 'jobs',
        element: <JobsPage />,
        children: [
          { index: true, element: <JobList /> },
          { path: 'new', element: <JobForm /> },
          { path: ':id', element: <JobDetailsPage /> },
          { path: ':id/edit', element: <JobForm /> }
        ]
      },
      // Other routes can be added here
    ]
  },
  // Add login and other public routes here
]);

export default router;