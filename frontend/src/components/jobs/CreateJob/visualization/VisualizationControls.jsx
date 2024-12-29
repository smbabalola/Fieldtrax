// File: /src/components/jobs/CreateJob/visualization/VisualizationControls.jsx
import React from 'react';
import { ButtonGroup, Button } from 'react-bootstrap';
import { FaSearchPlus, FaSearchMinus, FaExpand, FaCompress, FaRedo } from 'react-icons/fa';

const VisualizationControls = ({
  onZoomIn,
  onZoomOut,
  onReset,
  onToggleFullscreen,
  isFullscreen
}) => {
  return (
    <div className="visualization-controls">
      <ButtonGroup size="sm">
        <Button 
          variant="light" 
          onClick={onZoomIn}
          title="Zoom In"
        >
          <FaSearchPlus />
        </Button>
        <Button 
          variant="light" 
          onClick={onZoomOut}
          title="Zoom Out"
        >
          <FaSearchMinus />
        </Button>
        <Button 
          variant="light" 
          onClick={onReset}
          title="Reset View"
        >
          <FaRedo />
        </Button>
        <Button 
          variant="light" 
          onClick={onToggleFullscreen}
          title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
        >
          {isFullscreen ? <FaCompress /> : <FaExpand />}
        </Button>
      </ButtonGroup>
    </div>
  );
};

export default VisualizationControls;