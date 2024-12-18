//src/components/jobs/JobDetailsModal.jsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Modal, Row, Col, Table, Badge, Button, Spinner, Alert } from 'react-bootstrap';
import { selectJobDetailsModal, closeJobDetailsModal } from '../../store/slices/uiSlice';

const JobDetailsModal = () => {
  const dispatch = useDispatch();
  const { isOpen, selectedJob: job, loading, error } = useSelector(selectJobDetailsModal);

  const handleClose = () => {
    dispatch(closeJobDetailsModal());
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'Active': 'success',
      'Planned': 'warning',
      'Completed': 'info',
      'Cancelled': 'danger',
      'In Progress': 'primary'
    };
    return statusColors[status] || 'secondary';
  };

  const formatCurrency = (value) => {
    if (!value && value !== 0) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatNumber = (value, decimals = 2) => {
    if (!value && value !== 0) return 'N/A';
    return Number(value).toFixed(decimals);
  };

  if (!isOpen) return null;

  return (
    <Modal show={isOpen} onHide={handleClose} size="lg" backdrop="static">
      <Modal.Header closeButton>
        <Modal.Title className="d-flex align-items-center gap-2">
          {loading ? (
            <Spinner animation="border" size="sm" />
          ) : job ? (
            <>
              <span>{job.job_name}</span>
              <Badge bg={getStatusColor(job.status)}>
                {job.status}
              </Badge>
            </>
          ) : null}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body className="pb-0">
        {error ? (
          <Alert variant="danger">
            {error}
          </Alert>
        ) : loading ? (
          <div className="text-center py-4">
            <Spinner animation="border" />
            <p className="mt-2">Loading job details...</p>
          </div>
        ) : job ? (
          <>
            <div className="border-bottom mb-4">
              <h6 className="text-primary mb-3">Job Overview</h6>
              <Row className="mb-4">
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Job ID</td>
                        <td>{job.id}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Job Center</td>
                        <td>{job.job_center?.job_center_name || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Service Code</td>
                        <td>{job.service_code || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Description</td>
                        <td>{job.job_description || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Created Date</td>
                        <td>{formatDate(job.created_at)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Last Modified</td>
                        <td>{formatDate(job.updated_at)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Created By</td>
                        <td>{job.created_by || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Modified By</td>
                        <td>{job.updated_by || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </div>

            <div className="border-bottom mb-4">
              <h6 className="text-primary mb-3">Well Information</h6>
              <Row className="mb-4">
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Well Name</td>
                        <td>{job.well?.well_name || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">API Number</td>
                        <td>{job.well?.api_number || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Well Type</td>
                        <td>{job.well?.well_type || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Field Name</td>
                        <td>{job.well?.field_name || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Measured Depth</td>
                        <td>{formatNumber(job.measured_depth)} ft</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Total Vertical Depth</td>
                        <td>{formatNumber(job.total_vertical_depth)} ft</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Bottom Hole Temperature</td>
                        <td>{formatNumber(job.well?.bottom_hole_temperature)} °F</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Location</td>
                        <td>{job.well?.location || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </div>

            <div className="border-bottom mb-4">
              <h6 className="text-primary mb-3">Operator Information</h6>
              <Row className="mb-4">
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Operator Name</td>
                        <td>{job.operator?.operator_name || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Company Code</td>
                        <td>{job.operator?.company_code || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Contact Person</td>
                        <td>{job.operator?.contact_person || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Email</td>
                        <td>{job.operator?.email || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Phone</td>
                        <td>{job.operator?.phone_no_1 || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Alternative Phone</td>
                        <td>{job.operator?.phone_no_2 || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Address</td>
                        <td>{job.operator?.address || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Location</td>
                        <td>
                          {[job.operator?.city, job.operator?.state, job.operator?.country]
                            .filter(Boolean)
                            .join(', ') || 'N/A'}
                        </td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </div>

            <div className="border-bottom mb-4">
              <h6 className="text-primary mb-3">Schedule & Dates</h6>
              <Row className="mb-4">
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Spud Date</td>
                        <td>{formatDate(job.spud_date)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Mobilization Date</td>
                        <td>{formatDate(job.mobilization_date)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Expected Duration</td>
                        <td>{job.expected_duration || 'N/A'} days</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Completion Date</td>
                        <td>{formatDate(job.completion_date)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Demobilization Date</td>
                        <td>{formatDate(job.demobilization_date)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Actual Duration</td>
                        <td>{job.actual_duration || 'N/A'} days</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </div>

            <div className="mb-4">
              <h6 className="text-primary mb-3">Commercial Information</h6>
              <Row className="mb-4">
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">PO Number</td>
                        <td>{job.purchase_order?.po_number || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Contract Number</td>
                        <td>{job.purchase_order?.contract_no || 'N/A'}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Payment Terms</td>
                        <td>{job.purchase_order?.payment_terms || 'N/A'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
                <Col md={6}>
                  <Table bordered hover size="sm">
                    <tbody>
                      <tr>
                        <td className="fw-bold" width="40%">Estimated Value</td>
                        <td>{formatCurrency(job.estimated_value)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Actual Value</td>
                        <td>{formatCurrency(job.actual_value)}</td>
                      </tr>
                      <tr>
                        <td className="fw-bold">Currency</td>
                        <td>{job.currency || 'USD'}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </div>
          </>
        ) : null}
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        {job && job.status !== 'Completed' && (
          <Button variant="primary" onClick={() => window.location.href = `/jobs/${job.id}/edit`}>
            Edit Job
          </Button>
        )}
      </Modal.Footer>
    </Modal>
  );
};

export default JobDetailsModal;