// src/pages/job/JobLogs.jsx
import React from 'react';
import { Container, Card } from 'react-bootstrap';

const JobLogs = () => {
  return (
    <Container fluid>
      <h2 className="mb-4">Job Logs</h2>
      <Card>
        <Card.Body>Job logs will be displayed here</Card.Body>
      </Card>
    </Container>
  );
};

export default JobLogs;