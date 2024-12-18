// src/services/purchaseOrderService.js
import apiRequest, { API_ENDPOINTS, handleApiError } from '../utils/apiUtils';

const purchaseOrderService = {
  getPurchaseOrders: async (params = {}) => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.purchaseOrders.getAll, {
        params
      });
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching purchase orders');
    }
  },

  getPurchaseOrderById: async (id) => {
    try {
      const response = await apiRequest.get(API_ENDPOINTS.purchaseOrders.getById(id));
      return response.data; // Only return the data
    } catch (error) {
      handleApiError(error, 'Error fetching purchase order by id');
    }
  }
};

export default purchaseOrderService;