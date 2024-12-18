import React from 'react';
import { ButtonGroup, Button, Dropdown } from 'react-bootstrap';

const JobBulkActions = ({
  selectedCount = 0,
  onStatusChange = () => {},
  onExport = () => {},
  onDelete = () => {}
}) => {
  return (
    <div className="bg-light p-3 mb-3 border rounded">
      <div className="d-flex justify-content-between align-items-center">
        <div>
          <strong>{selectedCount}</strong> items selected
        </div>
        <ButtonGroup>
          <Dropdown as={ButtonGroup}>
            <Dropdown.Toggle variant="outline-primary" id="status-dropdown">
              Change Status
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item onClick={() => onStatusChange('Active')}>
                Set Active
              </Dropdown.Item>
              <Dropdown.Item onClick={() => onStatusChange('Planned')}>
                Set Planned
              </Dropdown.Item>
              <Dropdown.Item onClick={() => onStatusChange('Completed')}>
                Set Completed
              </Dropdown.Item>
              <Dropdown.Item onClick={() => onStatusChange('Cancelled')}>
                Set Cancelled
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          <Button 
            variant="outline-success"
            onClick={onExport}
          >
            <i className="bi bi-download me-1"></i>
            Export
          </Button>
          
          <Button 
            variant="outline-danger"
            onClick={onDelete}
          >
            <i className="bi bi-trash me-1"></i>
            Delete
          </Button>
        </ButtonGroup>
      </div>
    </div>
  );
};

export default JobBulkActions;