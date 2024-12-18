// File: /frontend/src/pages/jobs/Fluids/index.jsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Table, Button, Card } from 'react-bootstrap';
import { fetchFluids } from '../../../store/slices/fluidsSlice';
import CreateFluidModal from './CreateFluidModal';
import EditFluidModal from './EditFluidModal';

const Fluids = () => {
  const { jobId } = useParams();
  const dispatch = useDispatch();
  const { fluids, loading } = useSelector(state => state.fluids);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingFluid, setEditingFluid] = useState(null);

  useEffect(() => {
    if (jobId) {
      dispatch(fetchFluids(jobId));
    }
  }, [jobId, dispatch]);

  return (
    <Card className="mx-3 my-3">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <div>
          <h5 className="mb-0">Fluids</h5>
        </div>
        <Button 
          variant="primary" 
          size="sm"
          onClick={() => setShowCreateModal(true)}
        >
          Add Fluid
        </Button>
      </Card.Header>

      <Card.Body>
        {loading ? (
          <div className="text-center p-3">Loading...</div>
        ) : (
          <Table responsive striped bordered hover>
            <thead>
              <tr>
                <th>Type</th>
                <th>Volume (bbl)</th>
                <th>Density (ppg)</th>
                <th>Viscosity (cp)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {fluids.map((fluid) => (
                <tr key={fluid.id}>
                  <td>{fluid.type}</td>
                  <td>{fluid.volume}</td>
                  <td>{fluid.density}</td>
                  <td>{fluid.viscosity}</td>
                  <td>
                    <Button
                      variant="link"
                      size="sm"
                      onClick={() => setEditingFluid(fluid)}
                    >
                      Edit
                    </Button>
                  </td>
                </tr>
              ))}
              {fluids.length === 0 && (
                <tr>
                  <td colSpan="5" className="text-center">
                    No fluids added yet
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        )}
      </Card.Body>

      {/* Modals */}
      <CreateFluidModal
        show={showCreateModal}
        onHide={() => setShowCreateModal(false)}
        jobId={jobId}
      />

      {editingFluid && (
        <EditFluidModal
          show={true}
          fluid={editingFluid}
          onHide={() => setEditingFluid(null)}
          jobId={jobId}
        />
      )}
    </Card>
  );
};

export default Fluids;