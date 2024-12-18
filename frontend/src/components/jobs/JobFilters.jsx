// File: /frontend/src/components/jobs/JobFilters.jsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Card, Form, InputGroup, Row, Col, Button, Collapse } from 'react-bootstrap';
import { setFilter, resetFilters, selectJobsFilters } from '../../store/slices/jobsSlice';

const JOB_STATUSES = [
  { value: '', label: 'All Statuses' },
  { value: 'Active', label: 'Active' },
  { value: 'Planned', label: 'Planned' },
  { value: 'Completed', label: 'Completed' },
  { value: 'Cancelled', label: 'Cancelled' }
];

const JobFilters = ({ loading }) => {
  const dispatch = useDispatch();
  const filters = useSelector(selectJobsFilters);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterChange = (field, value) => {
    dispatch(setFilter({ [field]: value })); // Changed from setFilters to setFilter
  };

  const handleDateRangeChange = (field, value) => {
    dispatch(setFilter({  // Changed from setFilters to setFilter
      dateRange: {
        ...filters.dateRange,
        [field]: value
      }
    }));
  };

  const handleResetFilters = () => {
    dispatch(resetFilters());
  };

  return (
    <Card className="mb-4 shadow-sm">
      <Card.Header className="bg-white py-3">
        <Row className="align-items-center">
          <Col md={6} lg={8}>
            <InputGroup>
              <InputGroup.Text className="bg-light border-end-0">
                <i className="bi bi-search"></i>
              </InputGroup.Text>
              <Form.Control
                placeholder="Search jobs..."
                value={filters.search || ''}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                disabled={loading}
                className="border-start-0 ps-0"
              />
            </InputGroup>
          </Col>
          <Col md={4} lg={3}>
            <Form.Select
              value={filters.status || ''}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              disabled={loading}
            >
              {JOB_STATUSES.map(status => (
                <option key={status.value} value={status.value}>
                  {status.label}
                </option>
              ))}
            </Form.Select>
          </Col>
          <Col md={2} lg={1} className="text-end">
            <Button
              variant="link"
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-muted p-0"
              aria-expanded={isExpanded}
            >
              <i className={`bi bi-chevron-${isExpanded ? 'up' : 'down'}`}></i>
              <span className="d-none d-lg-inline ms-2">
                {isExpanded ? 'Less' : 'More'}
              </span>
            </Button>
          </Col>
        </Row>
      </Card.Header>

      <Collapse in={isExpanded}>
        <div>
          <Card.Body className="border-top bg-light">
            <Row className="g-3">
              {/* Operator Filter */}
              <Col md={4}>
                <Form.Group>
                  <Form.Label className="small text-muted">Operator</Form.Label>
                  <InputGroup>
                    <InputGroup.Text className="bg-white">
                      <i className="bi bi-building"></i>
                    </InputGroup.Text>
                    <Form.Control
                      placeholder="Filter by operator"
                      value={filters.operator || ''}
                      onChange={(e) => handleFilterChange('operator', e.target.value)}
                      disabled={loading}
                    />
                  </InputGroup>
                </Form.Group>
              </Col>

              {/* Rig Filter */}
              <Col md={4}>
                <Form.Group>
                  <Form.Label className="small text-muted">Rig</Form.Label>
                  <InputGroup>
                    <InputGroup.Text className="bg-white">
                      <i className="bi bi-gear"></i>
                    </InputGroup.Text>
                    <Form.Control
                      placeholder="Filter by rig"
                      value={filters.rig || ''}
                      onChange={(e) => handleFilterChange('rig', e.target.value)}
                      disabled={loading}
                    />
                  </InputGroup>
                </Form.Group>
              </Col>

              {/* Job Center Filter */}
              <Col md={4}>
                <Form.Group>
                  <Form.Label className="small text-muted">Job Center</Form.Label>
                  <InputGroup>
                    <InputGroup.Text className="bg-white">
                      <i className="bi bi-building-gear"></i>
                    </InputGroup.Text>
                    <Form.Control
                      placeholder="Filter by job center"
                      value={filters.jobCenter || ''}
                      onChange={(e) => handleFilterChange('jobCenter', e.target.value)}
                      disabled={loading}
                    />
                  </InputGroup>
                </Form.Group>
              </Col>

              {/* Date Range Filters */}
              <Col md={4}>
                <Form.Group>
                  <Form.Label className="small text-muted">Start Date</Form.Label>
                  <InputGroup>
                    <InputGroup.Text className="bg-white">
                      <i className="bi bi-calendar-event"></i>
                    </InputGroup.Text>
                    <Form.Control
                      type="date"
                      value={filters.dateRange?.from || ''}
                      onChange={(e) => handleDateRangeChange('from', e.target.value)}
                      disabled={loading}
                    />
                  </InputGroup>
                </Form.Group>
              </Col>

              <Col md={4}>
                <Form.Group>
                  <Form.Label className="small text-muted">End Date</Form.Label>
                  <InputGroup>
                    <InputGroup.Text className="bg-white">
                      <i className="bi bi-calendar-event"></i>
                    </InputGroup.Text>
                    <Form.Control
                      type="date"
                      value={filters.dateRange?.to || ''}
                      onChange={(e) => handleDateRangeChange('to', e.target.value)}
                      disabled={loading}
                    />
                  </InputGroup>
                </Form.Group>
              </Col>

              {/* Reset Filters */}
              <Col md={4} className="d-flex align-items-end">
                <Button
                  variant="outline-secondary"
                  onClick={handleResetFilters}
                  disabled={loading}
                  className="w-100"
                >
                  <i className="bi bi-x-circle me-2"></i>
                  Reset Filters
                </Button>
              </Col>
            </Row>
          </Card.Body>
        </div>
      </Collapse>
    </Card>
  );
};

export default JobFilters;