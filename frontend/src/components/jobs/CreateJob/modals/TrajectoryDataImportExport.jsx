// File: src/components/jobs/CreateJob/modals/TrajectoryDataImportExport.jsx
import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';
import { FaUpload, FaDownload, FaFileExcel, FaFileCsv } from 'react-icons/fa';
import trajectoryDataService from '../../../../services/trajectoryDataService';

const TrajectoryDataImportExport = ({
  show,
  onHide,
  onImport,
  trajectoryData
}) => {
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState(null);
  const [importType, setImportType] = useState('csv');

  const handleFileImport = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setImporting(true);
    setError(null);

    try {
      let importedData;
      if (importType === 'csv') {
        importedData = await trajectoryDataService.importFromCSV(file);
      } else {
        importedData = await trajectoryDataService.importFromExcel(file);
      }

      const validationErrors = trajectoryDataService.validateImportedData(importedData);
      if (validationErrors.length > 0) {
        throw new Error(validationErrors.join('\n'));
      }

      onImport(importedData);
      onHide();
    } catch (error) {
      setError(error.message);
    } finally {
      setImporting(false);
    }
  };

  const handleExport = async (format) => {
    try {
      let blob;
      let filename;

      if (format === 'csv') {
        blob = trajectoryDataService.exportToCSV(trajectoryData);
        filename = 'trajectory_data.csv';
      } else {
        blob = trajectoryDataService.exportToExcel(trajectoryData);
        filename = 'trajectory_data.xlsx';
      }

      trajectoryDataService.downloadFile(blob, filename);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Import/Export Trajectory Data</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && (
          <Alert variant="danger" onClose={() => setError(null)} dismissible>
            {error}
          </Alert>
        )}

        <div className="mb-4">
          <h6>Import Data</h6>
          <Form.Group className="mb-3">
            <Form.Label>Import Format</Form.Label>
            <Form.Select
              value={importType}
              onChange={(e) => setImportType(e.target.value)}
              className="mb-3"
            >
              <option value="csv">CSV File</option>
              <option value="excel">Excel File</option>
            </Form.Select>

            <div className="d-grid">
              <Button
                variant="outline-primary"
                onClick={() => document.getElementById('trajectory-file-input').click()}
                disabled={importing}
              >
                <FaUpload className="me-2" />
                {importing ? 'Importing...' : 'Select File to Import'}
              </Button>
              <Form.Control
                id="trajectory-file-input"
                type="file"
                accept={importType === 'csv' ? '.csv' : '.xlsx,.xls'}
                className="d-none"
                onChange={handleFileImport}
              />
            </div>
          </Form.Group>
        </div>

        <div>
          <h6>Export Data</h6>
          <div className="d-flex gap-2">
            <Button
              variant="outline-success"
              onClick={() => handleExport('csv')}
              disabled={!trajectoryData?.length}
              className="w-50"
            >
              <FaFileCsv className="me-2" />
              Export as CSV
            </Button>
            <Button
              variant="outline-success"
              onClick={() => handleExport('excel')}
              disabled={!trajectoryData?.length}
              className="w-50"
            >
              <FaFileExcel className="me-2" />
              Export as Excel
            </Button>
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default TrajectoryDataImportExport;