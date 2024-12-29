// File: /src/components/jobs/CreateJob/visualization/WellboreVisualization.jsx
import React, { useEffect, useState, useRef } from 'react';
import { Card } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import VisualizationControls from './VisualizationControls';
import { selectCasings, selectLiners } from '../../../../store/slices/wellboreGeometrySlice';

const WellboreVisualization = () => {
    const casings = useSelector(selectCasings);
    const liners = useSelector(selectLiners);
    const svgRef = useRef(null);
    const containerRef = useRef(null);
    
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const [transform, setTransform] = useState({ x: 0, y: 0, scale: 1 });
    const [isDragging, setIsDragging] = useState(false);
    const [startDragPos, setStartDragPos] = useState({ x: 0, y: 0 });
    const [isFullscreen, setIsFullscreen] = useState(false);

    useEffect(() => {
        const updateDimensions = () => {
          if (containerRef.current) {
            const { width } = containerRef.current.getBoundingClientRect();
            setDimensions({
              width: width,
              height: width * 2 // 1:2 aspect ratio
            });
          }
        };
    
        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
      }, [isFullscreen]);
    
      const handleMouseDown = (e) => {
        if (e.button === 0) { // Left click only
          setIsDragging(true);
          setStartDragPos({
            x: e.clientX - transform.x,
            y: e.clientY - transform.y
          });
        }
      };
    
      const handleMouseMove = (e) => {
        if (isDragging) {
          setTransform(prev => ({
            ...prev,
            x: e.clientX - startDragPos.x,
            y: e.clientY - startDragPos.y
          }));
        }
      };
    
      const handleMouseUp = () => {
        setIsDragging(false);
      };
    
      const handleZoomIn = () => {
        setTransform(prev => ({
          ...prev,
          scale: prev.scale * 1.2
        }));
      };
    
      const handleZoomOut = () => {
        setTransform(prev => ({
          ...prev,
          scale: Math.max(0.1, prev.scale / 1.2)
        }));
      };
    
      const handleReset = () => {
        setTransform({ x: 0, y: 0, scale: 1 });
      };
    
      const handleToggleFullscreen = () => {
        if (!isFullscreen) {
          if (containerRef.current.requestFullscreen) {
            containerRef.current.requestFullscreen();
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          }
        }
        setIsFullscreen(!isFullscreen);
      };
    
      const handleWheel = (e) => {
        e.preventDefault();
        const delta = Math.sign(e.deltaY);
        const scaleFactor = 1.1;
        
        setTransform(prev => ({
          ...prev,
          scale: delta > 0 ? 
            Math.max(0.1, prev.scale / scaleFactor) : 
            prev.scale * scaleFactor
        }));
      };
    
      useEffect(() => {
        const handleFullscreenChange = () => {
          setIsFullscreen(!!document.fullscreenElement);
        };
    
        document.addEventListener('fullscreenchange', handleFullscreenChange);
        return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
      }, []);

  const calculateScale = () => {
    if (!casings.length && !liners.length) return 1;

    const allTubulars = [...casings, ...liners];
    const maxDepth = Math.max(...allTubulars.map(t => t.end_depth));
    const maxDiameter = Math.max(...allTubulars.map(t => t.outer_diameter));

    const verticalScale = (dimensions.height - 2 * padding) / maxDepth;
    const horizontalScale = (dimensions.width - 2 * padding) / (maxDiameter * 2);

    return Math.min(verticalScale, horizontalScale);
  };

  const renderWellbore = () => {
    const sortedCasings = [...casings].sort((a, b) => b.outer_diameter - a.outer_diameter);
    const sortedLiners = [...liners].sort((a, b) => b.outer_diameter - a.outer_diameter);
    const currentScale = calculateScale();

    return (
      <g transform={`translate(${dimensions.width / 2}, ${padding})`}>
        {/* Draw surface line */}
        <line 
          x1={-dimensions.width/3} 
          x2={dimensions.width/3} 
          y1={0} 
          y2={0} 
          stroke="black" 
          strokeWidth="2"
        />

        {/* Draw casings */}
        {sortedCasings.map((casing, index) => (
          <g key={`casing-${index}`} className="casing">
            {/* Left side of casing */}
            <line
              x1={-(casing.outer_diameter/2) * currentScale}
              y1={casing.start_depth * currentScale}
              x2={-(casing.outer_diameter/2) * currentScale}
              y2={casing.end_depth * currentScale}
              stroke="blue"
              strokeWidth="2"
            />
            {/* Right side of casing */}
            <line
              x1={(casing.outer_diameter/2) * currentScale}
              y1={casing.start_depth * currentScale}
              x2={(casing.outer_diameter/2) * currentScale}
              y2={casing.end_depth * currentScale}
              stroke="blue"
              strokeWidth="2"
            />
            {/* Bottom of casing */}
            <line
              x1={-(casing.outer_diameter/2) * currentScale}
              y1={casing.end_depth * currentScale}
              x2={(casing.outer_diameter/2) * currentScale}
              y2={casing.end_depth * currentScale}
              stroke="blue"
              strokeWidth="2"
            />
            {/* Labels */}
            <text
              x={(casing.outer_diameter/2 + 10) * currentScale}
              y={(casing.start_depth + 20) * currentScale}
              fontSize="12"
              fill="black"
            >
              {`${casing.outer_diameter}" OD`}
            </text>
          </g>
        ))}

        {/* Draw liners */}
        {sortedLiners.map((liner, index) => (
          <g key={`liner-${index}`} className="liner">
            {/* Left side of liner */}
            <line
              x1={-(liner.outer_diameter/2) * currentScale}
              y1={liner.start_depth * currentScale}
              x2={-(liner.outer_diameter/2) * currentScale}
              y2={liner.end_depth * currentScale}
              stroke="green"
              strokeWidth="2"
              strokeDasharray="5,5"
            />
            {/* Right side of liner */}
            <line
              x1={(liner.outer_diameter/2) * currentScale}
              y1={liner.start_depth * currentScale}
              x2={(liner.outer_diameter/2) * currentScale}
              y2={liner.end_depth * currentScale}
              stroke="green"
              strokeWidth="2"
              strokeDasharray="5,5"
            />
            {/* Bottom of liner */}
            <line
              x1={-(liner.outer_diameter/2) * currentScale}
              y1={liner.end_depth * currentScale}
              x2={(liner.outer_diameter/2) * currentScale}
              y2={liner.end_depth * currentScale}
              stroke="green"
              strokeWidth="2"
            />
            {/* Labels */}
            <text
              x={(liner.outer_diameter/2 + 10) * currentScale}
              y={(liner.start_depth + 20) * currentScale}
              fontSize="12"
              fill="black"
            >
              {`${liner.outer_diameter}" Liner`}
            </text>
          </g>
        ))}

        {/* Depth markers */}
        <g className="depth-markers">
          {[...Array(10)].map((_, i) => {
            const depth = i * Math.ceil(Math.max(...casings.map(c => c.end_depth)) / 10);
            return (
              <g key={`depth-${i}`}>
                <line
                  x1={-20}
                  y1={depth * currentScale}
                  x2={20}
                  y2={depth * currentScale}
                  stroke="#999"
                  strokeWidth="1"
                />
                <text
                  x={-40}
                  y={depth * currentScale}
                  fontSize="10"
                  textAnchor="end"
                  alignmentBaseline="middle"
                >
                  {depth.toFixed(0)} ft
                </text>
              </g>
            );
          })}
        </g>
      </g>
    );
  };

  return (
    <Card className="mb-4">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <h5 className="mb-0">Wellbore Visualization</h5>
        <VisualizationControls
          onZoomIn={handleZoomIn}
          onZoomOut={handleZoomOut}
          onReset={handleReset}
          onToggleFullscreen={handleToggleFullscreen}
          isFullscreen={isFullscreen}
        />
      </Card.Header>
      <Card.Body>
        <div 
          ref={containerRef}
          className={`wellbore-visualization ${isFullscreen ? 'fullscreen' : ''}`}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onWheel={handleWheel}
        >
          <svg
            ref={svgRef}
            width="100%"
            height={dimensions.height}
            viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
            preserveAspectRatio="xMidYMid meet"
          >
            <g transform={`translate(${transform.x}, ${transform.y}) scale(${transform.scale})`}>
              {renderWellbore()}
            </g>
          </svg>
        </div>
      </Card.Body>
    </Card>
  );
};

export default WellboreVisualization;