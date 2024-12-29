// File: /src/hooks/useVisualizationControls.js
import { useState, useCallback, useEffect } from 'react';

const useVisualizationControls = (initialScale = 1, minScale = 0.1, maxScale = 5) => {
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: initialScale });
  const [isDragging, setIsDragging] = useState(false);
  const [startDragPos, setStartDragPos] = useState({ x: 0, y: 0 });

  const handleZoomIn = useCallback(() => {
    setTransform(prev => ({
      ...prev,
      scale: Math.min(maxScale, prev.scale * 1.2)
    }));
  }, [maxScale]);

  const handleZoomOut = useCallback(() => {
    setTransform(prev => ({
      ...prev,
      scale: Math.max(minScale, prev.scale / 1.2)
    }));
  }, [minScale]);

  const handleReset = useCallback(() => {
    setTransform({ x: 0, y: 0, scale: initialScale });
  }, [initialScale]);

  const handleMouseDown = useCallback((e) => {
    if (e.button === 0) { // Left click only
      setIsDragging(true);
      setStartDragPos({
        x: e.clientX - transform.x,
        y: e.clientY - transform.y
      });
    }
  }, [transform.x, transform.y]);

  const handleMouseMove = useCallback((e) => {
    if (isDragging) {
      setTransform(prev => ({
        ...prev,
        x: e.clientX - startDragPos.x,
        y: e.clientY - startDragPos.y
      }));
    }
  }, [isDragging, startDragPos]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleWheel = useCallback((e) => {
    e.preventDefault();
    const delta = Math.sign(e.deltaY);
    const scaleFactor = 1.1;
    
    setTransform(prev => ({
      ...prev,
      scale: delta > 0 ? 
        Math.max(minScale, prev.scale / scaleFactor) : 
        Math.min(maxScale, prev.scale * scaleFactor)
    }));
  }, [minScale, maxScale]);

  return {
    transform,
    isDragging,
    handlers: {
      handleMouseDown,
      handleMouseMove,
      handleMouseUp,
      handleZoomIn,
      handleZoomOut,
      handleReset,
      handleWheel
    }
  };
};

export default useVisualizationControls;