import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Button,
  Card,
  CardHeader,
  CardContent,
  CardTitle,
} from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Settings2 } from 'lucide-react';

const ColumnSelector = () => {
  const dispatch = useDispatch();
  const [isOpen, setIsOpen] = useState(false);
  
  // Default columns configuration
  const defaultColumns = {
    jobId: { title: 'Job ID', enabled: true },
    wellName: { title: 'Well Name', enabled: true },
    operator: { title: 'Operator', enabled: true },
    status: { title: 'Status', enabled: true },
    startDate: { title: 'Start Date', enabled: true },
    endDate: { title: 'End Date', enabled: true },
    location: { title: 'Location', enabled: false },
    rigName: { title: 'Rig Name', enabled: false },
    jobType: { title: 'Job Type', enabled: false },
    crew: { title: 'Crew', enabled: false },
    equipment: { title: 'Equipment', enabled: false },
    notes: { title: 'Notes', enabled: false }
  };

  const [selectedColumns, setSelectedColumns] = useState(() => {
    const savedColumns = localStorage.getItem('jobTableColumns');
    return savedColumns ? JSON.parse(savedColumns) : defaultColumns;
  });

  // Save column selection to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('jobTableColumns', JSON.stringify(selectedColumns));
    // Dispatch column changes to Redux store
    dispatch({ 
      type: 'jobs/updateColumnVisibility', 
      payload: selectedColumns 
    });
  }, [selectedColumns, dispatch]);

  const handleColumnToggle = (columnKey) => {
    setSelectedColumns(prev => ({
      ...prev,
      [columnKey]: {
        ...prev[columnKey],
        enabled: !prev[columnKey].enabled
      }
    }));
  };

  const handleReset = () => {
    setSelectedColumns(defaultColumns);
  };

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        className="flex items-center gap-2"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Settings2 className="h-4 w-4" />
        Columns
      </Button>

      {isOpen && (
        <Card className="absolute right-0 top-12 z-50 w-64 shadow-lg">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Table Columns</CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-72 pr-4">
              <div className="space-y-4">
                {Object.entries(selectedColumns).map(([key, column]) => (
                  <div key={key} className="flex items-center space-x-2">
                    <Checkbox
                      id={key}
                      checked={column.enabled}
                      onCheckedChange={() => handleColumnToggle(key)}
                    />
                    <label
                      htmlFor={key}
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      {column.title}
                    </label>
                  </div>
                ))}
              </div>
            </ScrollArea>
            <div className="mt-4 flex justify-end">
              <Button
                variant="outline"
                size="sm"
                onClick={handleReset}
                className="mr-2"
              >
                Reset
              </Button>
              <Button
                size="sm"
                onClick={() => setIsOpen(false)}
              >
                Done
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ColumnSelector;