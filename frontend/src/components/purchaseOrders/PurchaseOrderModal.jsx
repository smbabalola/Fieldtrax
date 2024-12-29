// File: /src/components/purchaseOrders/PurchaseOrderModal.jsx
import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Alert, Spinner } from 'react-bootstrap';
import purchaseOrderService from '../../services/purchaseOrderService';
import { toast } from 'react-toastify';

const initialFormState = {
  well_id: '',
  po_number: '',
  contract_no: '',
  vendor_no: '',
  DRSS_no: '',
  po_date: new Date().toISOString().split('T')[0],
  supplier_name: '',
  supplier_address1: '',
  supplier_address2: '',
  county: '',
  country: '',
  supplier_contact: '',
  supplier_contact_information: '',
  buyer_name: '',
  buyer_address1: '',
  buyer_address_2: '',
  buyer_contact_information: '',
  delievry_address1: '',
  delivery_address2: '',
  delievry_postcode: '',
  delivery_zipcode: '',
  payment_terms: '',
  shipping_terms: ''
};

const PurchaseOrderModal = ({ show, onHide, onSuccess, wellId = '' }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState(initialFormState);

  useEffect(() => {
    if (wellId) {
      setFormData(prev => ({
        ...prev,
        well_id: wellId
      }));
    }
  }, [wellId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (error) setError(null);
  };

  const validateForm = () => {
    const requiredFields = [
      'po_number',
      'supplier_name',
      'delievry_address1',
      'well_id'
    ];

    const missingFields = requiredFields.filter(field => !formData[field]);
    if (missingFields.length > 0) {
      setError(`Please fill in required fields: ${missingFields.join(', ')}`);
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    try {
      console.log('Submitting PO data:', formData);
      
      const response = await purchaseOrderService.createPurchaseOrder({
        ...formData,
        well_id: wellId || formData.well_id,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        po_date: formData.po_date ? new Date(formData.po_date).toISOString() : new Date().toISOString()
      });

      console.log('PO creation response:', response);
      
      toast.success('Purchase Order created successfully');
      onSuccess(response);
      onHide();
      setFormData(initialFormState);
    } catch (err) {
      console.error('PO creation error:', err);
      const errorDetail = err.response?.data?.detail || err.message;
      setError(`Failed to create purchase order: ${errorDetail}`);
      toast.error(`Error: ${errorDetail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Create Purchase Order</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && (
          <Alert variant="danger" onClose={() => setError(null)} dismissible>
            {error}
          </Alert>
        )}
        <Form onSubmit={handleSubmit}>
          {/* Required Fields Section */}
          <div className="mb-4 p-3 border rounded bg-light">
            <h6 className="mb-3 text-primary">Required Fields</h6>
            <div className="row">
              <div className="col-md-6">
                <Form.Group className="mb-3">
                  <Form.Label>PO Number<span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    name="po_number"
                    value={formData.po_number}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </div>
              <div className="col-md-6">
                <Form.Group className="mb-3">
                  <Form.Label>Well ID<span className="text-danger">*</span></Form.Label>
                  <Form.Control
                    type="text"
                    name="well_id"
                    value={formData.well_id || wellId}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </div>
            </div>
          </div>

          {/* Supplier Information */}
          <h5 className="mt-3 border-bottom pb-2">Supplier Information</h5>
          <div className="row">
            <div className="col-md-6">
              <Form.Group className="mb-3">
                <Form.Label>Supplier Name<span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  name="supplier_name"
                  value={formData.supplier_name}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </div>
            <div className="col-md-6">
              <Form.Group className="mb-3">
                <Form.Label>Supplier Contact</Form.Label>
                <Form.Control
                  type="text"
                  name="supplier_contact"
                  value={formData.supplier_contact}
                  onChange={handleChange}
                />
              </Form.Group>
            </div>
          </div>

          {/* Delivery Information */}
          <h5 className="mt-3 border-bottom pb-2">Delivery Information</h5>
          <div className="row">
            <div className="col-md-12">
              <Form.Group className="mb-3">
                <Form.Label>Delivery Address 1<span className="text-danger">*</span></Form.Label>
                <Form.Control
                  type="text"
                  name="delievry_address1"
                  value={formData.delievry_address1}
                  onChange={handleChange}
                  required
                />
              </Form.Group>
            </div>
          </div>

          {/* Additional Information */}
          <h5 className="mt-3 border-bottom pb-2">Additional Information</h5>
          <div className="row">
            <div className="col-md-6">
              <Form.Group className="mb-3">
                <Form.Label>Contract No.</Form.Label>
                <Form.Control
                  type="text"
                  name="contract_no"
                  value={formData.contract_no}
                  onChange={handleChange}
                />
              </Form.Group>
            </div>
            <div className="col-md-6">
              <Form.Group className="mb-3">
                <Form.Label>DRSS No.</Form.Label>
                <Form.Control
                  type="text"
                  name="DRSS_no"
                  value={formData.DRSS_no}
                  onChange={handleChange}
                />
              </Form.Group>
            </div>
          </div>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={loading}>
          Cancel
        </Button>
        <Button 
          variant="primary" 
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <>
              <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
                className="me-2"
              />
              Creating...
            </>
          ) : (
            'Create Purchase Order'
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default PurchaseOrderModal;