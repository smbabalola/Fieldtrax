// File: /src/components/jobs/CreateJob/tabs/RigInfoTab.jsx
import React, { useState, useEffect } from 'react';
import { Card, Button, Form, Row, Col, Modal } from 'react-bootstrap';
import { FaPlus } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { DataTable } from '../../../common/DataTable';
import rigService from '../../../../services/rigService';

const RigInfoTab = ({ data, onUpdate, errors = {} }) => {
  // State
  const [loading, setLoading] = useState(false);
  const [rigs, setRigs] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newRig, setNewRig] = useState({
    rig_name: '',
    contractor: '',
    rig_type: '',
    air_gap: '',
    water_depth: '',
    status: 'ACTIVE'
  });

  // Filters State
  const [filters, setFilters] = useState({
    searchTerm: '',
    contractor: '',
    rig_type: '',
    status: 'ALL'
  });

  const [sorting, setSorting] = useState({
    field: 'rig_name',
    direction: 'asc'
  });

  // Load Rigs
  useEffect(() => {
    const fetchRigs = async () => {
      try {
        setLoading(true);
        const response = await rigService.getAllRigs();
        setRigs(Array.isArray(response) ? response : []);
      } catch (error) {
        toast.error('Failed to load rigs');
        console.error('Error loading rigs:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRigs();
  }, []);

  // Column Definitions
  const columns = [
    { field: 'rig_name', header: 'Rig Name', sortable: true },
    { field: 'contractor', header: 'Contractor', sortable: true },
    { field: 'rig_type', header: 'Rig Type', sortable: true },
    { field: 'air_gap', header: 'Air Gap', sortable: true },
    { field: 'water_depth', header: 'Water Depth', sortable: true },
    { field: 'status', header: 'Status', sortable: true }
  ];

  // Filter Rigs
  const getFilteredRigs = () => {
    return rigs.filter(rig => {
      const matchesSearch = !filters.searchTerm || 
        rig.rig_name.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
        rig.contractor.toLowerCase().includes(filters.searchTerm.toLowerCase());
      
      const matchesContractor = !filters.contractor || 
        rig.contractor === filters.contractor;
      
      const matchesType = !filters.rig_type || 
        rig.rig_type === filters.rig_type;
      
      const matchesStatus = filters.status === 'ALL' || 
        rig.status === filters.status;

      return matchesSearch && matchesContractor && matchesType && matchesStatus;
    });
  };

  // Sort Rigs
  const getSortedRigs = (filteredRigs) => {
    return [...filteredRigs].sort((a, b) => {
      const aValue = a[sorting.field];
      const bValue = b[sorting.field];
      
      if (typeof aValue === 'string') {
        return sorting.direction === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }
      
      return sorting.direction === 'asc' 
        ? aValue - bValue 
        : bValue - aValue;
    });
  };

  // Handlers
  const handleSort = (field) => {
    setSorting(prev => ({
      field,
      direction: prev.field === field && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const handleRigSelect = (rig) => {
    onUpdate('rig', {
      rig_id: rig.id,
      rig_name: rig.rig_name
    });
  };

  const handleCreateRig = async () => {
    try {
      if (!newRig.rig_name || !newRig.contractor || !newRig.rig_type) {
        toast.error('Please fill in all required fields');
        return;
      }

      const response = await rigService.createRig(newRig);
      setRigs(prev => [...prev, response]);
      handleRigSelect(response);
      setShowCreateModal(false);
      setNewRig({
        rig_name: '',
        contractor: '',
        rig_type: '',
        air_gap: '',
        water_depth: '',
        status: 'ACTIVE'
      });
      toast.success('Rig created successfully');
    } catch (error) {
      toast.error(error.message || 'Failed to create rig');
    }
  };

  // Get unique values for filters
  const contractors = [...new Set(rigs.map(rig => rig.contractor))];
  const rigTypes = [...new Set(rigs.map(rig => rig.rig_type))];

  // Filter and sort the rigs
  const filteredRigs = getFilteredRigs();
  const sortedRigs = getSortedRigs(filteredRigs);

  return (
    <div>
      {/* Selection Summary */}
      <Card className="mb-4">
        <Card.Body>
          <Row>
            <Col md={6}>
              <Form.Group>
                <Form.Label>Selected Rig</Form.Label>
                <div className="d-flex gap-2">
                  <Form.Control
                    type="text"
                    value={rigs.find(r => r.id === data.rig_id)?.rig_name || ''}
                    readOnly
                    placeholder="Select a rig from the table below"
                    isInvalid={!!errors.rig_id}
                  />
                  <Button
                    variant="outline-primary"
                    onClick={() => setShowCreateModal(true)}
                  >
                    <FaPlus className="me-2" />
                    Add New
                  </Button>
                </div>
                <Form.Control.Feedback type="invalid">
                  {errors.rig_id}
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Filters */}
      <Card className="mb-4">
        <Card.Body>
          <Row>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Search</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Search rigs..."
                  value={filters.searchTerm}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    searchTerm: e.target.value
                  }))}
                />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Contractor</Form.Label>
                <Form.Select
                  value={filters.contractor}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    contractor: e.target.value
                  }))}
                >
                  <option value="">All Contractors</option>
                  {contractors.map(contractor => (
                    <option key={contractor} value={contractor}>
                      {contractor}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Rig Type</Form.Label>
                <Form.Select
                  value={filters.rig_type}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    rig_type: e.target.value
                  }))}
                >
                  <option value="">All Types</option>
                  {rigTypes.map(type => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Status</Form.Label>
                <Form.Select
                  value={filters.status}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    status: e.target.value
                  }))}
                >
                  <option value="ALL">All Status</option>
                  <option value="ACTIVE">Active</option>
                  <option value="INACTIVE">Inactive</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Rigs Table */}
      <DataTable
        columns={columns}
        data={sortedRigs}
        loading={loading}
        onRowClick={handleRigSelect}
        sortField={sorting.field}
        sortDirection={sorting.direction}
        onSort={handleSort}
      />

      {/* Create Rig Modal */}
      <Modal show={showCreateModal} onHide={() => setShowCreateModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Create New Rig</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Rig Name <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    value={newRig.rig_name}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      rig_name: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Contractor <span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    value={newRig.contractor}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      contractor: e.target.value
                    }))}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Rig Type <span className="text-danger">*</span></Form.Label>
                  <Form.Select
                    value={newRig.rig_type}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      rig_type: e.target.value
                    }))}
                    required
                  >
                    <option value="">Select Type</option>
                    <option value="JACKUP">Jackup</option>
                    <option value="SEMI_SUBMERSIBLE">Semi-Submersible</option>
                    <option value="DRILLSHIP">Drillship</option>
                    <option value="PLATFORM">Platform</option>
                    <option value="LAND">Land</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Status</Form.Label>
                  <Form.Select
                    value={newRig.status}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      status: e.target.value
                    }))}
                  >
                    <option value="ACTIVE">Active</option>
                    <option value="INACTIVE">Inactive</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Air Gap (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    value={newRig.air_gap}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      air_gap: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Water Depth (ft)</Form.Label>
                  <Form.Control
                    type="number"
                    value={newRig.water_depth}
                    onChange={(e) => setNewRig(prev => ({
                      ...prev,
                      water_depth: e.target.value
                    }))}
                  />
                </Form.Group>
              </Col>
            </Row>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowCreateModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleCreateRig}>
            Create Rig
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default RigInfoTab;