// File: /frontend/src/pages/job/tabs/components/ActivityList.jsx
import React from 'react';
import { Card, Badge } from 'react-bootstrap';

const getActivityTypeColor = (type) => {
  const colors = {
    mobilization: 'primary',
    demobilization: 'secondary',
    equipment_delivery: 'info',
    start_job: 'success',
    end_job: 'warning',
    incident: 'danger',
    NPT: 'dark'
  };
  return colors[type] || 'secondary';
};

const ActivityList = ({ activities }) => {
  return (
    <div className="activity-list mt-4">
      <h5 className="mb-3">Activity History</h5>
      <div className="timeline">
        {activities && activities.length > 0 ? (
          activities.map((activity, index) => (
            <Card key={activity.id || index} className="mb-3 border-0 shadow-sm">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <div>
                    <Badge bg={getActivityTypeColor(activity.type)} className="mb-2">
                      {activity.type.replace('_', ' ').toUpperCase()}
                    </Badge>
                    <p className="mb-1">{activity.description}</p>
                    <small className="text-muted">
                      By {activity.user?.name || 'Unknown User'} • 
                      {new Date(activity.timestamp).toLocaleString()}
                    </small>
                  </div>
                </div>
              </Card.Body>
            </Card>
          ))
        ) : (
          <Card className="border-0 shadow-sm">
            <Card.Body className="text-center text-muted">
              <p className="mb-0">No activities recorded yet</p>
            </Card.Body>
          </Card>
        )}
      </div>
      
      <style jsx>{`
        .timeline {
          position: relative;
          padding: 1rem 0;
        }
        
        .timeline::before {
          content: '';
          position: absolute;
          top: 0;
          left: 1rem;
          height: 100%;
          width: 2px;
          background: #e9ecef;
        }
      `}</style>
    </div>
  );
};

export default ActivityList;