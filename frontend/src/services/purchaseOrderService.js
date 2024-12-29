// File: /src/services/purchaseOrderService.js
import api, { API_ENDPOINTS, handleApiError } from './api';

// Utility function for date formatting
const formatDate = (date) => {
  if (!date) return new Date().toISOString();
  try {
    return new Date(date).toISOString();
  } catch (e) {
    console.error('Date formatting error:', e);
    return new Date().toISOString();
  }
};

// Transform PO data for API
const transformPOData = (data) => ({
  created_at: formatDate(data.created_at || new Date()),
  updated_at: formatDate(data.updated_at || new Date()),
  well_id: data.well_id || null,
  po_number: data.po_number || '',
  contract_no: data.contract_no || '',
  vendor_no: data.vendor_no || '',
  DRSS_no: data.DRSS_no || '',
  po_date: formatDate(data.po_date),
  supplier_name: data.supplier_name || '',
  supplier_address1: data.supplier_address1 || '',
  supplier_address2: data.supplier_address2 || '',
  county: data.county || '',
  country: data.country || '',
  supplier_contact: data.supplier_contact || '',
  supplier_contact_information: data.supplier_contact_information || '',
  buyer_name: data.buyer_name || '',
  buyer_address1: data.buyer_address1 || '',
  buyer_address2: data.buyer_address2 || '',
  buyer_contact_information: data.buyer_contact_information || '',
  delivery_address1: data.delivery_address1 || '',
  delivery_address2: data.delivery_address2 || '',
  delivery_postcode: data.delivery_postcode || '',
  delivery_zipcode: data.delivery_zipcode || '',
  payment_terms: data.payment_terms || '',
  shipping_terms: data.shipping_terms || '',
  status: data.status || 'draft',
  total_amount: Number(data.total_amount) || 0,
  currency: data.currency || 'USD'
});

const purchaseOrderService = {
  // Core PO Operations
  getPurchaseOrders: async (params = {}) => {
    try {
      const queryParams = {
        skip: params.page ? (params.page - 1) * (params.limit || 10) : 0,
        limit: params.limit || 10,
        status: params.status,
        well_id: params.well_id,
        start_date: params.start_date ? formatDate(params.start_date) : undefined,
        end_date: params.end_date ? formatDate(params.end_date) : undefined,
        sort_by: params.sort_by || 'po_date',
        sort_direction: params.sort_direction || 'desc',
        ...params.filters
      };

      const response = await api.get(API_ENDPOINTS.purchaseOrders.getAll, { params: queryParams });
      
      return {
        items: Array.isArray(response.items) ? response.items : [],
        total: response.total || 0,
        page: params.page || 1,
        pageSize: params.limit || 10,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 10))
      };
    } catch (error) {
      return handleApiError(error, 'Error fetching purchase orders');
    }
  },

  getPurchaseOrderById: async (id) => {
    try {
      const response = await api.get(API_ENDPOINTS.purchaseOrders.getById(id));
      return response;
    } catch (error) {
      return handleApiError(error, 'Error fetching purchase order details');
    }
  },

  createPurchaseOrder: async (poData) => {
    try {
      // Validate required fields
      const validation = purchaseOrderService.validatePOData(poData);
      if (!validation.isValid) {
        throw new Error(`Validation failed: ${JSON.stringify(validation.errors)}`);
      }

      const formattedData = transformPOData(poData);
      console.log('Sending PO data to API:', formattedData);
      
      const response = await api.post(API_ENDPOINTS.purchaseOrders.base, formattedData);
      return response;
    } catch (error) {
      console.error('PO creation error:', error);
      throw error;
    }
  },

  updatePurchaseOrder: async (id, poData) => {
    try {
      const formattedData = transformPOData(poData);
      const response = await api.put(`${API_ENDPOINTS.purchaseOrders.base}/${id}`, formattedData);
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating purchase order');
    }
  },

  deletePurchaseOrder: async (id) => {
    try {
      await api.delete(`${API_ENDPOINTS.purchaseOrders.base}/${id}`);
      return true;
    } catch (error) {
      return handleApiError(error, 'Error deleting purchase order');
    }
  },

  // PO Items Operations
  addPurchaseOrderItem: async (poId, itemData) => {
    try {
      const response = await api.post(
        `${API_ENDPOINTS.purchaseOrders.base}/${poId}/items`,
        itemData
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error adding purchase order item');
    }
  },

  updatePurchaseOrderItem: async (poId, itemId, itemData) => {
    try {
      const response = await api.put(
        `${API_ENDPOINTS.purchaseOrders.base}/${poId}/items/${itemId}`,
        itemData
      );
      return response;
    } catch (error) {
      return handleApiError(error, 'Error updating purchase order item');
    }
  },

  deletePurchaseOrderItem: async (poId, itemId) => {
    try {
      await api.delete(`${API_ENDPOINTS.purchaseOrders.base}/${poId}/items/${itemId}`);
      return true;
    } catch (error) {
      return handleApiError(error, 'Error deleting purchase order item');
    }
  },

  getPurchaseOrderItems: async (poId) => {
    try {
      const response = await api.get(`${API_ENDPOINTS.purchaseOrders.base}/${poId}/items`);
      return Array.isArray(response) ? response : [];
    } catch (error) {
      return handleApiError(error, 'Error fetching purchase order items');
    }
  },

  // PO Status Operations
  updatePurchaseOrderStatus: async (id, status, notes = '') => {
    try {
      const response = await api.put(`/purchase-orders/${id}/status`, { status, notes });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error updating purchase order status');
    }
  },

  submitForApproval: async (id) => {
    try {
      const response = await api.post(`/purchase-orders/${id}/submit`);
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error submitting purchase order for approval');
    }
  },

  approvePurchaseOrder: async (id, approverNotes = '') => {
    try {
      const response = await api.post(`/purchase-orders/${id}/approve`, { approverNotes });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error approving purchase order');
    }
  },

  rejectPurchaseOrder: async (id, rejectionReason) => {
    try {
      const response = await api.post(`/purchase-orders/${id}/reject`, { rejectionReason });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error rejecting purchase order');
    }
  },

  generatePODocument: async (id, format = 'pdf') => {
    try {
      const response = await api.get(`/purchase-orders/${id}/document`, { params: { format } });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error generating purchase order document');
    }
  },

  // Batch Operations
  batchUpdatePurchaseOrders: async (updates) => {
    try {
      const response = await api.put('/purchase-orders/batch-update', updates);
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error batch updating purchase orders');
    }
  },

  // Statistics and Reports
  getPurchaseOrderStatistics: async (params = {}) => {
    try {
      const response = await api.get('/purchase-orders/statistics', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error fetching purchase order statistics');
    }
  },

  // Validation
  validatePOData: (data) => {
    const errors = {};

    // Required fields validation
    if (!data.po_number?.trim()) {
      errors.po_number = 'PO number is required';
    }

    if (!data.supplier_name?.trim()) {
      errors.supplier_name = 'Supplier name is required';
    }

    if (!data.po_date) {
      errors.po_date = 'PO date is required';
    }

    // Numeric validations
    if (data.total_amount && isNaN(Number(data.total_amount))) {
      errors.total_amount = 'Total amount must be a number';
    }

    // Date validations
    try {
      if (data.po_date) new Date(data.po_date);
    } catch (e) {
      errors.po_date = 'Invalid PO date format';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  },

  // Search and Filter
  searchPurchaseOrders: async (searchParams) => {
    try {
      const response = await api.get('/purchase-orders/search', { params: searchParams });
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error searching purchase orders');
    }
  },

  /**
   * Get purchase orders by vendor number
   * @param {string} vendorNo Vendor number
   * @returns {Promise<Array>} List of purchase orders
   */
  getPurchaseOrdersByVendor: async (vendorNo) => {
    try {
      const response = await api.get(`/purchase-orders/vendor/${vendorNo}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error fetching purchase orders by vendor');
    }
  },

  /**
   * Get purchase orders by contract number
   * @param {string} contractNo Contract number
   * @returns {Promise<Array>} List of purchase orders
   */
  getPurchaseOrdersByContract: async (contractNo) => {
    try {
      const response = await api.get(`/purchase-orders/contract/${contractNo}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response.data.message || 'Error fetching purchase orders by contract');
    }
  },

  getById: (id) => api.get(API_ENDPOINTS.purchaseOrders.getById(id)),
  create: (data) => api.post(API_ENDPOINTS.purchaseOrders.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.purchaseOrders.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.purchaseOrders.delete(id))
};

export default purchaseOrderService;