// File: /frontend/src/components/DataGrid/DataGrid.example.jsx
import React from 'react';
import DataGrid from './DataGrid';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const DataGridExample = () => {
  // Sample data
  const data = [
    { id: 1, name: 'Well A', type: 'Oil', status: 'Active', depth: 5000 },
    { id: 2, name: 'Well B', type: 'Gas', status: 'Planned', depth: 6000 },
    { id: 3, name: 'Well C', type: 'Water', status: 'Complete', depth: 4500 },
  ];

  // Column definitions
  const columns = [
    { 
      key: 'name', 
      label: 'Well Name',
      filterable: true 
    },
    { 
      key: 'type', 
      label: 'Well Type',
      filterable: true 
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => (
        <span className={`badge ${
          row.status === 'Active' ? 'bg-success' :
          row.status === 'Planned' ? 'bg-primary' :
          'bg-secondary'
        }`}>
          {row.status}
        </span>
      ),
      filterable: true
    },
    { 
      key: 'depth', 
      label: 'Depth (ft)',
      render: (row) => row.depth.toLocaleString() 
    },
  ];

  // Example custom actions
  const customActions = (
    <>
      <button className="btn btn-outline-primary me-2">
        <i className="bi bi-plus-lg me-2"></i>
        Add Well
      </button>
      <button className="btn btn-outline-secondary">
        <i className="bi bi-download me-2"></i>
        Export
      </button>
    </>
  );

  // Example row click handler
  const handleRowClick = (row) => {
    console.log('Row clicked:', row);
  };

  // Example export handler
  const handleExport = (data) => {
    console.log('Exporting data:', data);
    // Implement export logic here
  };

  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col">
          <h1 className="h3">Wells Overview</h1>
        </div>
      </div>
      
      <div className="row">
        <div className="col">
          <div className="card">
            <div className="card-body">
              <DataGrid
                data={data}
                columns={columns}
                pageSize={10}
                selectable={true}
                onRowClick={handleRowClick}
                actions={customActions}
                exportable={true}
                onExport={handleExport}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataGridExample;