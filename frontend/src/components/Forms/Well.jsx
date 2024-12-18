
// File: /frontend/src/pages/job/Well.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import WellForm from '../../components/Forms/WellForm';
import WellSummary from '../../components/Well/WellSummary';
import WellTrajectoryChart from '../../components/Charts/WellTrajectoryChart';
import DataGrid from '../../components/DataGrid/DataGrid';
import wellService from '../../services/wellService';

const Well = () => {
  const { jobId } = useParams();
  const [wellData, setWellData] = useState(null);
  const [trajectoryData, setTrajectoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [well, trajectory] = await Promise.all([
          wellService.getWellbore(jobId),
          wellService.getTrajectory(jobId)
        ]);
        setWellData(well);
        setTrajectoryData(trajectory);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [jobId]);

  const handleUpdateWell = async (formData) => {
    try {
      await wellService.updateWellbore(jobId, formData);
      const updatedWell = await wellService.getWellbore(jobId);
      setWellData(updatedWell);
      setIsEditing(false);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div className="flex justify-center p-8">Loading...</div>;
  }

  if (error) {
    return (
      <Alert variant="destructive" className="m-4">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Well Information</h1>
        <Button 
          onClick={() => setIsEditing(!isEditing)}
          className="bg-blue-500 text-white"
        >
          {isEditing ? 'Cancel' : 'Edit Well'}
        </Button>
      </div>

      {isEditing ? (
        <Card className="p-6">
          <WellForm 
            initialData={wellData}
            onSubmit={handleUpdateWell}
            isLoading={loading}
          />
        </Card>
      ) : (
        <WellSummary wellData={wellData} />
      )}

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Well Trajectory</h2>
        <WellTrajectoryChart trajectoryData={trajectoryData} />
      </Card>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Operations History</h2>
        <DataGrid 
          data={wellData.operations || []}
          columns={[
            { key: 'date', label: 'Date' },
            { key: 'operation', label: 'Operation' },
            { key: 'duration', label: 'Duration (hrs)' },
            { key: 'status', label: 'Status' }
          ]}
          pageSize={5}
        />
      </Card>
    </div>
  );
};

export default Well;
