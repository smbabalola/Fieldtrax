
// File: /frontend/src/components/Well/WellSummary.jsx
import React from 'react';
import { Card } from '@/components/ui/card';

const WellSummary = ({ wellData }) => {
  return (
    <Card className="p-4">
      <h3 className="text-lg font-medium mb-4">Well Summary</h3>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600">Well Name</p>
          <p className="font-medium">{wellData.wellName}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Well Type</p>
          <p className="font-medium">{wellData.wellType}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Status</p>
          <p className="font-medium">{wellData.status}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Total Depth</p>
          <p className="font-medium">{wellData.totalDepth} ft</p>
        </div>
      </div>
    </Card>
  );
};

export default WellSummary;
