
// File: /frontend/src/components/Well/WellHeader.jsx
import React from 'react';

const WellHeader = ({ wellData }) => {
  return (
    <div className="bg-white p-4 shadow rounded-lg">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold">{wellData.wellName}</h2>
          <p className="text-gray-600">API: {wellData.apiNumber}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Current Status</p>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            {wellData.status}
          </span>
        </div>
      </div>
    </div>
  );
};

export default WellHeader;