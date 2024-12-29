// File: src/components/Forms/WellTrajectoryChart.jsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Label,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ZAxis
} from "recharts";

const WellTrajectoryChart = ({
  trajectoryData,
  mode = '2D',
  showGrid = true,
  showLabels = true,
  onPointClick
}) => {
  // Data processing for different visualizations
  const getChartData = () => {
    if (!trajectoryData || trajectoryData.length === 0) return [];

    return trajectoryData.map(point => ({
      id: point.id,
      md: point.measured_depth,
      tvd: point.true_vertical_depth,
      ns: point.northing,
      ew: point.easting,
      vs: point.vertical_section,
      inc: point.inclination,
      az: point.azimuth,
      dls: point.dog_leg_severity
    }));
  };

  const get2DData = () => {
    const data = getChartData();
    return data.map(point => ({
      ...point,
      x: point.ew,  // East-West as X
      y: point.tvd  // TVD as Y
    }));
  };

  const renderVerticalSection = () => (
    <ResponsiveContainer width="100%" height={500}>
      <LineChart
        data={getChartData()}
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey="vs" reversed>
          {showLabels && <Label value="Vertical Section (ft)" position="bottom" />}
        </XAxis>
        <YAxis reversed>
          {showLabels && <Label value="TVD (ft)" position="left" angle={-90} />}
        </YAxis>
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="tvd"
          stroke="#8884d8"
          dot={{ onClick: (e, payload) => onPointClick?.(trajectoryData[payload.index]) }}
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );

  const render2DView = () => (
    <ResponsiveContainer width="100%" height={500}>
      <ScatterChart
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey="x" type="number">
          {showLabels && <Label value="East-West (ft)" position="bottom" />}
        </XAxis>
        <YAxis dataKey="y" reversed>
          {showLabels && <Label value="TVD (ft)" position="left" angle={-90} />}
        </YAxis>
        <ZAxis range={[100]} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Legend />
        <Scatter
          name="Well Path"
          data={get2DData()}
          fill="#8884d8"
          line={{ stroke: '#8884d8' }}
          lineType="joint"
          onClick={(e) => {
            if (e && e.id) {
              const point = trajectoryData.find(p => p.id === e.id);
              if (point) onPointClick?.(point);
            }
          }}
        />
      </ScatterChart>
    </ResponsiveContainer>
  );

  const renderInclinationProfile = () => (
    <ResponsiveContainer width="100%" height={500}>
      <LineChart
        data={getChartData()}
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        {showGrid && <CartesianGrid strokeDasharray="3 3" />}
        <XAxis dataKey="md">
          {showLabels && <Label value="Measured Depth (ft)" position="bottom" />}
        </XAxis>
        <YAxis>
          {showLabels && <Label value="Inclination (°)" position="left" angle={-90} />}
        </YAxis>
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="inc"
          stroke="#82ca9d"
          dot={{ onClick: (e, payload) => onPointClick?.(trajectoryData[payload.index]) }}
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );

  // Select visualization based on mode
  const renderVisualization = () => {
    switch (mode) {
      case '2D':
        return render2DView();
      case 'VS':
        return renderVerticalSection();
      case 'INC':
        return renderInclinationProfile();
      default:
        return render2DView();
    }
  };

  return (
    <div className="well-trajectory-chart">
      {trajectoryData.length === 0 ? (
        <div className="text-center p-5 text-muted">
          No trajectory data available
        </div>
      ) : (
        renderVisualization()
      )}
    </div>
  );
};

export default WellTrajectoryChart;