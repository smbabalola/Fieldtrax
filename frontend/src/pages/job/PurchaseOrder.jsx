// src/pages/job/PurchaseOrder.jsx
import React from 'react';
import { Container, Card } from 'react-bootstrap';

const PurchaseOrder = () => {
  return (
    <Container fluid>
      <h2 className="mb-4">Purchase Orders</h2>
      <Card>
        <Card.Body>Purchase order information will be displayed here</Card.Body>
      </Card>
    </Container>
  );
};

export default PurchaseOrder;