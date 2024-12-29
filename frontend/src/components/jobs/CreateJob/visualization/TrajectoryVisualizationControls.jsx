import React from 'react';
import { ButtonGroup, Button, Form } from 'react-bootstrap';
import { 
  FaCube, 
  FaSquare, 
  FaThLarge, 
  FaTags,
  FaSave,
  FaExpand,
  FaCompress
} from 'react-icons/fa';

const TrajectoryVisualizationControls = ({
  mode,
  onModeChange,
  showGrid,
  onToggleGrid,
  showLabels,
  onToggleLabels,
  isFullscreen,
  onToggleFullscreen,
  onSaveImage
}) => {
  return (
    <div className="d-flex justify-content-between align-items-center">
      <div className="visualization-controls">
        <ButtonGroup className="me-3">
          <Button
            variant={mode === '2D' ? 'primary' : 'outline-primary'}
            onClick={() => onModeChange('2D')}
            title="2D View"
          >
            <FaSquare className="me-1" /> 2D
          </Button>
          <Button
            variant={mode === '3D' ? 'primary' : 'outline-primary'}
            onClick={() => onModeChange('3D')}
            title="3D View"
          >
            <FaCube className="me-1" /> 3D
          </Button>
        </ButtonGroup>

        <ButtonGroup className="me-3">
          <Button
            variant={showGrid ? 'primary' : 'outline-primary'}
            onClick={() => onToggleGrid(!showGrid)}
            title="Toggle Grid"
          >
            <FaThLarge />
          </Button>
          <Button
            variant={showLabels ? 'primary' : 'outline-primary'}
            onClick={() => onToggleLabels(!showLabels)}
            title="Toggle Labels"
          >
            <FaTags />
          </Button>
        </ButtonGroup>

        <ButtonGroup>
          <Button
            variant="outline-secondary"
            onClick={onSaveImage}
            title="Save Image"
          >
            <FaSave />
          </Button>
          <Button
            variant="outline-secondary"
            onClick={onToggleFullscreen}
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <FaCompress /> : <FaExpand />}
          </Button>
        </ButtonGroup>
      </div>

      <div className="visualization-settings">
        <Form.Group className="mb-0">
          <Form.Select 
            size="sm" 
            style={{ width: 'auto' }}
            onChange={(e) => onModeChange(e.target.value)}
            value={mode}
          >
            <option value="2D">Vertical Section</option>
            <option value="2D-NS">North-South Section</option>
            <option value="2D-EW">East-West Section</option>
            <option value="3D">3D View</option>
          </Form.Select>
        </Form.Group>
      </div>
    </div>
  );
};

export default TrajectoryVisualizationControls;