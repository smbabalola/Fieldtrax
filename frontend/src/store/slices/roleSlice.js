// src/store/slices/roleSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import roleService from '../../services/roleService';
import { cacheService } from '../../services/cacheService';

// Async Thunks
export const fetchRoles = createAsyncThunk(
  'roles/fetchRoles',
  async (params, { rejectWithValue }) => {
    try {
      const cacheKey = `roles_${JSON.stringify(params)}`;
      const cached = cacheService.get(cacheKey);
      if (cached) return cached;

      const response = await roleService.getRoles(params);
      cacheService.set(cacheKey, response, 5);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const createRole = createAsyncThunk(
  'roles/createRole',
  async (roleData, { rejectWithValue }) => {
    try {
      const response = await roleService.createRole(roleData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateRole = createAsyncThunk(
  'roles/updateRole',
  async ({ roleId, roleData }, { rejectWithValue }) => {
    try {
      const response = await roleService.updateRole(roleId, roleData);
      cacheService.clear();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const deleteRole = createAsyncThunk(
  'roles/deleteRole',
  async (roleId, { rejectWithValue }) => {
    try {
      await roleService.deleteRole(roleId);
      cacheService.clear();
      return roleId;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const assignRoleToUser = createAsyncThunk(
  'roles/assignRoleToUser',
  async ({ userId, roleId }, { rejectWithValue }) => {
    try {
      const response = await roleService.assignRoleToUser(userId, roleId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const removeRoleFromUser = createAsyncThunk(
  'roles/removeRoleFromUser',
  async ({ userId, roleId }, { rejectWithValue }) => {
    try {
      const response = await roleService.removeRoleFromUser(userId, roleId);
      return { userId, roleId };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const addPermissionToRole = createAsyncThunk(
  'roles/addPermissionToRole',
  async ({ roleId, permissionId }, { rejectWithValue }) => {
    try {
      const response = await roleService.addPermissionToRole(roleId, permissionId);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const removePermissionFromRole = createAsyncThunk(
  'roles/removePermissionFromRole',
  async ({ roleId, permissionId }, { rejectWithValue }) => {
    try {
      const response = await roleService.removePermissionFromRole(roleId, permissionId);
      return { roleId, permissionId };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialFilters = {
  searchTerm: '',
  type: 'ALL',
  status: 'ALL'
};

// Initial State
const initialState = {
  roles: [],
  selectedRole: null,
  userRoles: {},
  rolePermissions: {},
  loading: false,
  roleDetailsLoading: false,
  error: null,
  roleDetailsError: null,
  filters: initialFilters,
  pagination: {
    currentPage: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  sorting: {
    field: 'name',
    order: 'asc'
  },
  lastUpdated: null
};

// Slice
const roleSlice = createSlice({
  name: 'roles',
  initialState,
  reducers: {
    clearRoleDetails: (state) => {
      state.selectedRole = null;
      state.roleDetailsError = null;
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
      state.roleDetailsError = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch Roles
      .addCase(fetchRoles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRoles.fulfilled, (state, action) => {
        state.loading = false;
        state.roles = action.payload.items || [];
        state.pagination = {
          currentPage: action.payload.page || 1,
          pageSize: action.payload.page_size || 10,
          totalItems: action.payload.total || 0,
          totalPages: action.payload.total_pages || 0
        };
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchRoles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch roles';
        state.roles = [];
      })

      // Create Role
      .addCase(createRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createRole.fulfilled, (state, action) => {
        state.loading = false;
        state.roles.unshift(action.payload);
        state.pagination.totalItems += 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(createRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Update Role
      .addCase(updateRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateRole.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.roles.findIndex(role => role.id === action.payload.id);
        if (index !== -1) {
          state.roles[index] = action.payload;
        }
        if (state.selectedRole?.id === action.payload.id) {
          state.selectedRole = action.payload;
        }
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(updateRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Delete Role
      .addCase(deleteRole.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteRole.fulfilled, (state, action) => {
        state.loading = false;
        state.roles = state.roles.filter(role => role.id !== action.payload);
        if (state.selectedRole?.id === action.payload) {
          state.selectedRole = null;
        }
        state.pagination.totalItems -= 1;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(deleteRole.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // Assign Role to User
      .addCase(assignRoleToUser.fulfilled, (state, action) => {
        const { userId, roleId } = action.payload;
        if (!state.userRoles[userId]) {
          state.userRoles[userId] = [];
        }
        if (!state.userRoles[userId].includes(roleId)) {
          state.userRoles[userId].push(roleId);
        }
      })

      // Remove Role from User
      .addCase(removeRoleFromUser.fulfilled, (state, action) => {
        const { userId, roleId } = action.payload;
        if (state.userRoles[userId]) {
          state.userRoles[userId] = state.userRoles[userId].filter(id => id !== roleId);
        }
      })

      // Add Permission to Role
      .addCase(addPermissionToRole.fulfilled, (state, action) => {
        const { roleId, permissionId } = action.payload;
        if (!state.rolePermissions[roleId]) {
          state.rolePermissions[roleId] = [];
        }
        if (!state.rolePermissions[roleId].includes(permissionId)) {
          state.rolePermissions[roleId].push(permissionId);
        }
      })

      // Remove Permission from Role
      .addCase(removePermissionFromRole.fulfilled, (state, action) => {
        const { roleId, permissionId } = action.payload;
        if (state.rolePermissions[roleId]) {
          state.rolePermissions[roleId] = state.rolePermissions[roleId]
            .filter(id => id !== permissionId);
        }
      });
  }
});

// Action Creators
export const {
  clearRoleDetails,
  setFilter,
  resetFilters,
  setSorting,
  setPage,
  setPageSize,
  clearErrors
} = roleSlice.actions;

// Basic Selectors
export const selectRoles = state => state.roles.roles;
export const selectSelectedRole = state => state.roles.selectedRole;
export const selectUserRoles = state => state.roles.userRoles;
export const selectRolePermissions = state => state.roles.rolePermissions;
export const selectLoading = state => state.roles.loading;
export const selectError = state => state.roles.error;
export const selectPagination = state => state.roles.pagination;
export const selectFilters = state => state.roles.filters;
export const selectSorting = state => state.roles.sorting;
export const selectLastUpdated = state => state.roles.lastUpdated;

// Complex Selectors
export const selectFilteredRoles = state => {
  const roles = selectRoles(state);
  const filters = selectFilters(state);
  
  return roles.filter(role => {
    const matchesSearch = !filters.searchTerm || 
      role.name?.toLowerCase().includes(filters.searchTerm.toLowerCase()) ||
      role.description?.toLowerCase().includes(filters.searchTerm.toLowerCase());
    
    const matchesType = filters.type === 'ALL' || role.type === filters.type;
    const matchesStatus = filters.status === 'ALL' || role.status === filters.status;

    return matchesSearch && matchesType && matchesStatus;
  });
};

export const selectRoleById = (state, roleId) => 
  state.roles.roles.find(role => role.id === roleId);

export const selectUserRolesByUserId = (state, userId) => 
  state.roles.userRoles[userId] || [];

export const selectRolePermissionsByRoleId = (state, roleId) =>
  state.roles.rolePermissions[roleId] || [];

export const selectIsUserInRole = (state, userId, roleId) =>
  state.roles.userRoles[userId]?.includes(roleId) || false;

export default roleSlice.reducer;