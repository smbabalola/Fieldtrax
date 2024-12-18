// src/pages/MainDashboard.jsx
import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { 
  Tools, 
  ClockFill, 
  FileText, 
  PeopleFill 
} from 'react-bootstrap-icons';

const MainDashboard = () => {
  const stats = [
    {
      title: 'Active Jobs',
      value: '12',
      icon: <Tools size={24} className="text-primary" />,
      change: '+2 this month'
    },
    {
      title: 'Total Hours',
      value: '284',
      icon: <ClockFill size={24} className="text-primary" />,
      change: '32 this week'
    },
    {
      title: 'Field Reports',
      value: '18',
      icon: <FileText size={24} className="text-primary" />,
      change: '5 pending'
    },
    {
      title: 'Field Personnel',
      value: '24',
      icon: <PeopleFill size={24} className="text-primary" />,
      change: '8 on site'
    }
  ];

  return (
    <Container fluid>
      {/* Header */}
      <Row className="mb-4">
        <Col>
          <h1>Dashboard</h1>
          <p className="text-muted">Welcome to FieldTrax</p>
        </Col>
      </Row>

      {/* Stats Cards */}
      <Row className="g-4 mb-4">
        {stats.map((stat, index) => (
          <Col md={3} key={index}>
            <Card>
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 className="text-muted mb-2">{stat.title}</h6>
                    <h2 className="mb-0">{stat.value}</h2>
                    <small className="text-muted">{stat.change}</small>
                  </div>
                  <div>{stat.icon}</div>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Overview Card */}
      <Row>
        <Col>
          <Card>
            <Card.Header className="bg-white">
              <h5 className="mb-0">Overview</h5>
            </Card.Header>
            <Card.Body>
              <p>Your field operations at a glance. System is ready for operations.</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default MainDashboard;