// src/pages/job/Fluid.jsx
import React from 'react';
import { Container, Card } from 'react-bootstrap';

const Fluid = () => {
  return (
    <Container fluid>
      <h2 className="mb-4">Fluid Management</h2>
      <Card>
        <Card.Body>Fluid management information will be displayed here</Card.Body>
      </Card>
    </Container>
  );
};

export default Fluid;