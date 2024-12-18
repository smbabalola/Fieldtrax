// File: /frontend/src/components/jobs/ColumnSettings.jsx
import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Modal, Button, Form, ListGroup } from 'react-bootstrap';
import { 
  toggleColumnVisibility, 
  reorderColumn, 
  resetColumnSettings,
  selectTableColumns,
  selectColumnSettingsOpen,
  toggleColumnSettings
} from '../../store/slices/uiSlice';

const ColumnSettings = () => {
  const dispatch = useDispatch();
  const columns = useSelector(selectTableColumns);
  const isOpen = useSelector(selectColumnSettingsOpen);
  const [localColumns, setLocalColumns] = useState([]);

  useEffect(() => {
    // Convert columns object to sorted array for display
    const sortedColumns = Object.entries(columns)
      .map(([id, config]) => ({
        id,
        ...config
      }))
      .sort((a, b) => a.order - b.order);
    
    setLocalColumns(sortedColumns);
  }, [columns]);

  const handleClose = () => {
    dispatch(toggleColumnSettings());
  };

  const handleReset = () => {
    dispatch(resetColumnSettings());
  };

  const handleVisibilityToggle = (columnId) => {
    dispatch(toggleColumnVisibility(columnId));
  };

  const moveColumn = (index, direction) => {
    const items = Array.from(localColumns);
    if (
      (direction === 'up' && index === 0) || 
      (direction === 'down' && index === items.length - 1)
    ) {
      return;
    }

    const newIndex = direction === 'up' ? index - 1 : index + 1;
    const [movedItem] = items.splice(index, 1);
    items.splice(newIndex, 0, movedItem);

    // Update order numbers
    items.forEach((item, idx) => {
      dispatch(reorderColumn({ columnId: item.id, newOrder: idx + 1 }));
    });

    setLocalColumns(items);
  };

  return (
    <Modal show={isOpen} onHide={handleClose} size="md">
      <Modal.Header closeButton>
        <Modal.Title>Customize Columns</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <ListGroup className="mb-3">
            {localColumns.map((column, index) => (
              <ListGroup.Item
                key={column.id}
                className="d-flex justify-content-between align-items-center"
              >
                <div className="d-flex align-items-center">
                  <Form.Check
                    type="checkbox"
                    id={`column-${column.id}`}
                    label={column.title}
                    checked={column.visible}
                    onChange={() => handleVisibilityToggle(column.id)}
                    className="mb-0 me-3"
                  />
                </div>
                <div className="d-flex">
                  <Button
                    variant="link"
                    size="sm"
                    onClick={() => moveColumn(index, 'up')}
                    disabled={index === 0}
                    className="p-0 me-2"
                  >
                    ↑
                  </Button>
                  <Button
                    variant="link"
                    size="sm"
                    onClick={() => moveColumn(index, 'down')}
                    disabled={index === localColumns.length - 1}
                    className="p-0"
                  >
                    ↓
                  </Button>
                </div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="outline-secondary" onClick={handleReset}>
          Reset to Default
        </Button>
        <Button variant="primary" onClick={handleClose}>
          Done
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ColumnSettings;