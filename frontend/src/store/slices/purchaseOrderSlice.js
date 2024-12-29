// src/store/slices/purchaseOrderSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import purchaseOrderService from '../../services/purchaseOrderService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchPurchaseOrders = createAsyncThunk(
  'purchaseOrders/fetchPurchaseOrders',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `purchase_orders_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await purchaseOrderService.getPurchaseOrders(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchPurchaseOrderById = createAsyncThunk(
  'purchaseOrders/fetchPurchaseOrderById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.getPurchaseOrderById(id);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createPurchaseOrder = createAsyncThunk(
  'purchaseOrders/createPurchaseOrder',
  async (poData, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.createPurchaseOrder(poData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updatePurchaseOrder = createAsyncThunk(
  'purchaseOrders/updatePurchaseOrder',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.updatePurchaseOrder(id, data);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deletePurchaseOrder = createAsyncThunk(
  'purchaseOrders/deletePurchaseOrder',
  async (id, { rejectWithValue }) => {
    try {
      await purchaseOrderService.deletePurchaseOrder(id);
      cacheService.clear();
      return id;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const submitForApproval = createAsyncThunk(
  'purchaseOrders/submitForApproval',
  async (id, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.submitForApproval(id);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const approvePurchaseOrder = createAsyncThunk(
  'purchaseOrders/approvePurchaseOrder',
  async ({ id, approverNotes }, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.approvePurchaseOrder(id, approverNotes);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const rejectPurchaseOrder = createAsyncThunk(
  'purchaseOrders/rejectPurchaseOrder',
  async ({ id, rejectionReason }, { rejectWithValue }) => {
    try {
      const response = await purchaseOrderService.rejectPurchaseOrder(id, rejectionReason);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  status: 'ALL',
  searchTerm: '',
  supplier: null,
  dateRange: {
    startDate: null,
    endDate: null
  },
  priceRange: {
    min: null,
    max: null
  }
};

// Initial State
const initialState = {
  purchaseOrders: [],
  selectedPurchaseOrder: null,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  loading: false,
  poDetailsLoading: false,
  error: null,
  poDetailsError: null,
  filters: initialFilters,
  sorting: {
    field: 'po_date',
    order: 'desc'
  },
  statistics: {
    totalAmount: 0,
    pendingApproval: 0,
    approved: 0,
    rejected: 0
  },
  lastUpdated: null
};

// Slice
const purchaseOrderSlice = createSlice({
  name: 'purchaseOrders',
  initialState,
  reducers: {
    clearPODetails: (state) => {
      state.selectedPurchaseOrder = null;
      state.poDetailsError = null;
    },
    setFilter: (state, action) => {
      state.filters = {
        ...state.filters,
        ...action.payload
      };
      state.pagination.currentPage = 1;
    },
    resetFilters: (state) => {
      state.filters = initialFilters;
      state.pagination.currentPage = 1;
    },
    setSorting: (state, action) => {
      state.sorting = action.payload;
      state.pagination.currentPage = 1;
    },
    setPage: (state, action) => {
      state.pagination.currentPage = action.payload;
    },
    setPageSize: (state, action) => {
      state.pagination.pageSize = action.payload;
      state.pagination.currentPage = 1;
    },
    clearErrors: (state) => {
      state.error = null;
      state.poDetailsError = null;
    },
    updateStatistics: (state, action) => {
      state.statistics = {
        ...state.statistics,
        ...action.payload
      };
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Purchase Orders
      .addCase(fetchPurchaseOrders.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPurchaseOrders.fulfilled, (state, action) => {
        state.loading = false;
        state.purchaseOrders = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchPurchaseOrders.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch purchase orders';
        state.purchaseOrders = [];
      })

      // Fetch Purchase Order Details
      .addCase(fetchPurchaseOrderById.pending, (state) => {
        state.poDetailsLoading = true;
        state.poDetailsError = null;
      })
      .addCase(fetchPurchaseOrderById.fulfilled, (state, action) => {
        state.poDetailsLoading = false;
        state.selectedPurchaseOrder = action.payload;
        state.poDetailsError = null;
      })
      .addCase(fetchPurchaseOrderById.rejected, (state, action) => {
        state.poDetailsLoading = false;
        state.poDetailsError = action.payload;
      })

      // Create Purchase Order
      .addCase(createPurchaseOrder.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createPurchaseOrder.fulfilled, (state, action) => {
        state.loading = false;
        state.purchaseOrders.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createPurchaseOrder.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Purchase Order
      .addCase(updatePurchaseOrder.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updatePurchaseOrder.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.purchaseOrders.findIndex(po => po.id === action.payload.id);
        if (index !== -1) {
          state.purchaseOrders[index] = action.payload;
        }
        if (state.selectedPurchaseOrder?.id === action.payload.id) {
          state.selectedPurchaseOrder = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updatePurchaseOrder.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Purchase Order
      .addCase(deletePurchaseOrder.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deletePurchaseOrder.fulfilled, (state, action) => {
        state.loading = false;
        state.purchaseOrders = state.purchaseOrders.filter(po => po.id !== action.payload);
        if (state.selectedPurchaseOrder?.id === action.payload) {
          state.selectedPurchaseOrder = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deletePurchaseOrder.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Submit For Approval
      .addCase(submitForApproval.fulfilled, (state, action) => {
        const index = state.purchaseOrders.findIndex(po => po.id === action.payload.id);
        if (index !== -1) {
          state.purchaseOrders[index] = action.payload;
        }
        if (state.selectedPurchaseOrder?.id === action.payload.id) {
          state.selectedPurchaseOrder = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
      })

      // Approve Purchase Order
      .addCase(approvePurchaseOrder.fulfilled, (state, action) => {
        const index = state.purchaseOrders.findIndex(po => po.id === action.payload.id);
        if (index !== -1) {
          state.purchaseOrders[index] = action.payload;
        }
        if (state.selectedPurchaseOrder?.id === action.payload.id) {
          state.selectedPurchaseOrder = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
      })

      // Reject Purchase Order
      .addCase(rejectPurchaseOrder.fulfilled, (state, action) => {
        const index = state.purchaseOrders.findIndex(po => po.id === action.payload.id);
        if (index !== -1) {
          state.purchaseOrders[index] = action.payload;
        }
        if (state.selectedPurchaseOrder?.id === action.payload.id) {
          state.selectedPurchaseOrder = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
      });
  }
});

// Action Creators
export const {
  clearPODetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors,
  updateStatistics
} = purchaseOrderSlice.actions;

// Basic Selectors
export const selectPurchaseOrders = state => state.purchaseOrders.purchaseOrders;
export const selectSelectedPO = state => state.purchaseOrders.selectedPurchaseOrder;
export const selectLoading = state => state.purchaseOrders.loading;
export const selectPODetailsLoading = state => state.purchaseOrders.poDetailsLoading;
export const selectError = state => state.purchaseOrders.error;
export const selectPODetailsError = state => state.purchaseOrders.poDetailsError;
export const selectPagination = state => state.purchaseOrders.pagination;
export const selectFilters = state => state.purchaseOrders.filters;
export const selectSorting = state => state.purchaseOrders.sorting;
export const selectStatistics = state => state.purchaseOrders.statistics;
export const selectLastUpdated = state => state.purchaseOrders.lastUpdated;

// Complex Selectors
export const selectFilteredPurchaseOrders = state => {
  const purchaseOrders = selectPurchaseOrders(state);
  const filters = selectFilters(state);
  
  return purchaseOrders.filter(po => {
    const matchesStatus = filters.status === 'ALL' || po.status === filters.status;
    const matchesSearch = !filters.searchTerm || 
      po.po_number?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      po.supplier_name?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesSupplier = !filters.supplier || po.supplier_id === filters.supplier;
    
    const matchesDateRange = !filters.dateRange.startDate || !filters.dateRange.endDate || 
      (new Date(po.po_date) >= new Date(filters.dateRange.startDate) &&
       new Date(po.po_date) <= new Date(filters.dateRange.endDate));

    const matchesPriceRange = (!filters.priceRange.min || po.total_amount >= filters.priceRange.min) &&
      (!filters.priceRange.max || po.total_amount <= filters.priceRange.max);

    return matchesStatus && matchesSearch && matchesSupplier && matchesDateRange && matchesPriceRange;
  });
};

export const selectPurchaseOrderById = (state, poId) => 
  state.purchaseOrders.purchaseOrders.find(po => po.id === poId);

export default purchaseOrderSlice.reducer;