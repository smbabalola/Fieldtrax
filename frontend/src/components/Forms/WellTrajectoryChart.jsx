// File: /frontend/src/components/Charts/WellTrajectoryChart.jsx
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

const WellTrajectoryChart = ({ trajectoryData }) => {
  return (
    <div className="w-full h-96">
      <LineChart
        width={800}
        height={400}
        data={trajectoryData}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="measureDepth" label="Measured Depth (ft)" />
        <YAxis label="True Vertical Depth (ft)" />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="trueVerticalDepth"
          stroke="#8884d8"
          name="TVD"
        />
      </LineChart>
    </div>
  );
};

export default WellTrajectoryChart;