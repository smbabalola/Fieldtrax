// File: /src/services/api.js
import axios from 'axios';
import store from '../store';
import { logout } from '../store/slices/authSlice';
import { toast } from 'react-toastify';

// API Endpoints configuration
const API_ENDPOINTS = {
  auth: {
    login: '/token',
    refresh: '/token/refresh',
    logout: '/auth/logout',
    verify: '/auth/verify',
    passwordResetRequest: '/auth/password-reset/request-reset',
    passwordReset: '/auth/password-reset/reset-password',
    changePassword: '/auth/change-password',
    verifyEmail: '/auth/verify-email',
    sendVerification: '/auth/send-verification'
  },
  fluids: {
    base: '/fluids',
    getByWellbore: (wellboreId) => `/fluids/wellbore/${wellboreId}`,
    getByType: (wellboreId, type) => `/fluids/wellbore/${wellboreId}/type/${type}`,
    update: (id) => `/fluids/${id}`
  },
  jobs: {
    base: '/jobs',
    getAll: '/jobs',
    getById: (id) => `/jobs/${id}`,
    create: '/jobs',
    update: (id) => `/jobs/${id}`,
    delete: (id) => `/jobs/${id}`,
    active: '/jobs/active',
    export: '/jobs/export'
  },
  operators: {
    base: '/operators',
    getAll: '/operators',
    getByName: (name) => `/operators/name/${name}`,
    getByCode: (code) => `/operators/code/${code}`,
    create: '/operators'
  },
  jobCenters: {
    base: '/job-centers',
    getAll: '/job-centers',
    getActive: '/job-centers/active',
    getByWell: (wellName) => `/job-centers/well/${wellName}`,
    getByShortName: (shortName) => `/job-centers/short/${shortName}`
  },
  wells: {
    base: '/wells',
    getAll: '/wells',
    getByOperator: (operatorId) => `/wells/operator/${operatorId}`,
    create: '/wells'
  },
  wellShapes: {
    base: '/well-shapes',
    getAll: '/well-shapes',
    create: '/well-shapes'
  },
  productionTypes: {
    base: '/production-types',
    getAll: '/production-types',
    create: '/production-types'
  },
  slots: {
    base: '/slots',
    getAll: '/slots',
    create: '/slots',
    getByInstallation: (installationId) => `/slots/installation/${installationId}`,
    getAvailable: (installationId) => `/slots/installation/${installationId}/available`,
    getWithWells: (installationId) => `/slots/installation/${installationId}/with-wells`,
    getStatistics: (installationId) => `/slots/installation/${installationId}/statistics`,
    getByCoordinates: (minEastings, maxEastings, minNorthings, maxNorthings) => `/slots/coordinates?minEastings=${minEastings}&maxEastings=${maxEastings}&minNorthings=${minNorthings}&maxNorthings=${maxNorthings}`,
    updateCoordinates: (slotId) => `/slots/${slotId}/coordinates`,
    batchCreate: '/slots/batch'
  },
  rigs: {
    base: '/rigs',
    getAll: '/rigs',
    getActive: '/rigs/active'
  },
  purchaseOrders: {
    base: '/purchase-orders',
    getAll: '/purchase-orders',
    getById: (id) => `/purchase-orders/${id}`,
    createPurchaseOrder: '/purchase-orders',
    create: '/purchase-orders'
  },
  roles: {
    base: '/roles',
    getAll: '/roles',
    getById: (roleId) => `/roles/${roleId}`,
    create: '/roles',
    update: (roleId) => `/roles/${roleId}`,
    delete: (roleId) => `/roles/${roleId}`,
    addPermission: (roleId, permissionId) => `/roles/${roleId}/permissions/${permissionId}`,
    removePermission: (roleId, permissionId) => `/roles/${roleId}/permissions/${permissionId}`
  },
  users: {
    base: '/users',
    getAll: '/users',
    getById: (userId) => `/users/${userId}`,
    create: '/users',
    update: (userId) => `/users/${userId}`,
    delete: (userId) => `/users/${userId}`,
    verifyEmail: '/users/verify-email',
    sendVerification: '/users/send-verification',
    changePassword: '/users/change-password'
  },
  activities: {
    base: '/activities',
    getByJob: (jobId) => `/activities/job/${jobId}`,
    getByDateRange: (jobId, startDate, endDate) => `/activities/job/${jobId}/date-range?start=${startDate}&end=${endDate}`,
    create: '/activities',
    update: (activityId) => `/activities/${activityId}`
  },
  contractTypes: {
    base: '/contract-types',
    getAll: '/contract-types',
    getByType: (contractType) => `/contract-types/type/${contractType}`,
    create: '/contract-types',
    update: (typeId) => `/contract-types/${typeId}`
  },
  dailyReports: {
    base: '/daily-reports',
    getByWellbore: (wellboreId) => `/daily-reports/wellbore/${wellboreId}`,
    create: '/daily-reports',
    update: (reportId) => `/daily-reports/${reportId}`
  },
  hangers: {
    base: '/hangers',
    getAll: '/hangers',
    getByWellbore: (wellboreId) => `/hangers/wellbore/${wellboreId}`,
    getByType: (wellboreId, hangerType) => `/hangers/wellbore/${wellboreId}/type/${hangerType}`,
    create: '/hangers',
    update: (hangerId) => `/hangers/${hangerId}`
  },
  installationTypes: {
    base: '/installation-types',
    getAll: '/installation-types',
    getByType: (installationType) => `/installation-types/type/${installationType}`,
    create: '/installation-types',
    update: (typeId) => `/installation-types/${typeId}`
  },
  installations: {
    base: '/installations',
    getByField: (fieldId) => `/installations/field/${fieldId}`,
    getByType: (typeId) => `/installations/type/${typeId}`,
    create: '/installations',
    update: (installationId) => `/installations/${installationId}`
  },
  jobParameters: {
    base: '/job-parameters',
    getByWellbore: (wellboreId) => `/job-parameters/wellbore/${wellboreId}`,
    create: '/job-parameters',
    update: (paramId) => `/job-parameters/${paramId}`
  },
  mudEquipmentDetails: {
    base: '/mud-equipment-details',
    getByReport: (reportId) => `/mud-equipment-details/report/${reportId}`,
    create: '/mud-equipment-details',
    update: (equipmentId) => `/mud-equipment-details/${equipmentId}`
  },
  mudPumpDetails: {
    base: '/mud-pump-details',
    getByReport: (reportId) => `/mud-pump-details/report/${reportId}`,
    getActive: (reportId) => `/mud-pump-details/report/${reportId}/active`,
    create: '/mud-pump-details',
    update: (pumpId) => `/mud-pump-details/${pumpId}`
  },
  operationalParameters: {
    base: '/operational-parameters',
    getByWellbore: (wellboreId) => `/operational-parameters/wellbore/${wellboreId}`,
    getByZone: (wellboreId, zone) => `/operational-parameters/wellbore/${wellboreId}/zone/${zone}`,
    create: '/operational-parameters',
    update: (paramId) => `/operational-parameters/${paramId}`
  },
  physicalBarriers: {
    base: '/physical-barriers',
    getByWellbore: (wellboreId) => `/physical-barriers/wellbore/${wellboreId}`,
    getVerified: (wellboreId) => `/physical-barriers/wellbore/${wellboreId}/verified`,
    create: '/physical-barriers',
    update: (barrierId) => `/physical-barriers/${barrierId}`
  },
  productions: {
    base: '/productions',
    getByType: (productionType) => `/productions/type/${productionType}`,
    create: '/productions',
    update: (productionId) => `/productions/${productionId}`
  },
  sealAssemblies: {
    base: '/seal-assemblies',
    getByWellbore: (wellboreId) => `/seal-assemblies/wellbore/${wellboreId}`,
    create: '/seal-assemblies',
    update: (assemblyId) => `/seal-assemblies/${assemblyId}`
  },
  settings: {
    base: '/settings',
    get: '/settings',
    update: '/settings',
    reset: '/settings/reset'
  },
  tallyItems: {
    base: '/tally-items',
    getByTally: (tallyId) => `/tally-items/tally/${tallyId}`,
    getBySerial: (serialNumber) => `/tally-items/serial/${serialNumber}`,
    calculateTotalLength: (tallyId) => `/tally-items/tally/${tallyId}/total-length`,
    create: '/tally-items',
    update: (itemId) => `/tally-items/${itemId}`
  },
  tallies: {
    base: '/tallies',
    getById: (tallyId) => `/tallies/${tallyId}`,
    create: '/tallies',
    update: (tallyId) => `/tallies/${tallyId}`
  },
  timeSheets: {
    base: '/time-sheets',
    getByJob: (jobId) => `/time-sheets/job/${jobId}`,
    getByEmployee: (employeeId) => `/time-sheets/employee/${employeeId}`,
    getPending: '/time-sheets/pending',
    getByDateRange: (startDate, endDate, employeeId) => `/time-sheets/date-range?start=${startDate}&end=${endDate}&employeeId=${employeeId}`,
    calculateTotalHours: (employeeId, startDate, endDate) => `/time-sheets/hours/total?employeeId=${employeeId}&start=${startDate}&end=${endDate}`,
    create: '/time-sheets',
    update: (timesheetId) => `/time-sheets/${timesheetId}`
  },
  trajectories: {
    base: '/trajectories',
    getByWellbore: (wellboreId) => `/trajectories/wellbore/${wellboreId}`,
    create: '/trajectories',
    update: (trajectoryId) => `/trajectories/${trajectoryId}`
  },
  tubularTypes: {
    base: '/tubular-types',
    getAll: '/tubular-types',
    getByName: (typeName) => `/tubular-types/type/${typeName}`,
    getByShortName: (shortName) => `/tubular-types/short/${shortName}`,
    create: '/tubular-types',
    update: (typeId) => `/tubular-types/${typeId}`
  },
  tubulars: {
    base: '/tubulars',
    getById: (tubularId) => `/tubulars/${tubularId}`,
    getByType: (tubulartypeId) => `/tubulars/type/${tubulartypeId}`,
    create: '/tubulars',
    update: (tubularId) => `/tubulars/${tubularId}`
  },
  casings: {
    base: '/casings',
    getById: (casingId) => `/casings/${casingId}`,
    getByCementTopRange: (minTop, maxTop) => `/casings/cement-top-range?minTop=${minTop}&maxTop=${maxTop}`,
    create: '/casings',
    update: (casingId) => `/casings/${casingId}`
  },
  liners: {
    base: '/liners',
    getById: (linerId) => `/liners/${linerId}`,
    getByOverlapRange: (minOverlap, maxOverlap) => `/liners/overlap-range?minOverlap=${minOverlap}&maxOverlap=${maxOverlap}`,
    create: '/liners',
    update: (linerId) => `/liners/${linerId}`
  },
  drillstrings: {
    base: '/drillstrings',
    getById: (drillstringId) => `/drillstrings/${drillstringId}`,
    getByComponentType: (componentType) => `/drillstrings/component-type/${componentType}`,
    create: '/drillstrings',
    update: (drillstringId) => `/drillstrings/${drillstringId}`
  },
  wellTypes: {
    base: '/well-types',
    getAll: '/well-types',
    getByType: (wellType) => `/well-types/type/${wellType}`,
    create: '/well-types',
    update: (typeId) => `/well-types/${typeId}`
  },
  wells: {
    base: '/wells',
    getAll: '/wells',
    getByOperator: (operatorId) => `/wells/operator/${operatorId}`,
    getBySlot: (slotId) => `/wells/slot/${slotId}`,
    getById: (wellId) => `/wells/${wellId}`,
    create: '/wells',
    update: (wellId) => `/wells/${wellId}`
  },
  wellbores: {
    base: '/wellbores',
    getAll: '/wellbores',
    getActive: '/wellbores/active',
    getPlanned: '/wellbores/planned',
    getCompleted: '/wellbores/completed',
    getByWell: (wellId) => `/wellbores/well/${wellId}`,
    getById: (wellboreId) => `/wellbores/${wellboreId}`,
    getByDateRange: (startDate, endDate) => `/wellbores/date-range?start=${startDate}&end=${endDate}`,
    getSummary: (wellboreId) => `/wellbores/${wellboreId}/summary`,
    calculateCosts: (wellboreId) => `/wellbores/${wellboreId}/costs`,
    create: '/wellbores',
    update: (wellboreId) => `/wellbores/${wellboreId}`
  },
  backloads: {
    base: '/backloads',
    getById: (backloadId) => `/backloads/${backloadId}`,
    getByWellbore: (wellboreId) => `/backloads/wellbore/${wellboreId}`,
    create: '/backloads',
    update: (backloadId) => `/backloads/${backloadId}`,
    approve: (backloadId) => `/backloads/${backloadId}/approve`,
    getPending: '/backloads/pending'
  },
  deliveryTickets: {
    base: '/delivery-tickets',
    getById: (ticketId) => `/delivery-tickets/${ticketId}`,
    getByNumber: (ticketNumber) => `/delivery-tickets/number/${ticketNumber}`,
    getByWellbore: (wellboreId) => `/delivery-tickets/wellbore/${wellboreId}`,
    getByPurchaseOrder: (poId) => `/delivery-tickets/purchase-order/${poId}`,
    getByDateRange: (startDate, endDate, wellboreId) => `/delivery-tickets/date-range?start=${startDate}&end=${endDate}&wellboreId=${wellboreId}`,
    create: '/delivery-tickets',
    update: (ticketId) => `/delivery-tickets/${ticketId}`,
    addItem: (ticketId) => `/delivery-tickets/${ticketId}/items`,
    getItems: (ticketId) => `/delivery-tickets/${ticketId}/items`
  },
  contractors: {
    base: '/contractors',
    getByName: (contractorName) => `/contractors/name/${contractorName}`,
    getByCountry: (country) => `/contractors/country/${country}`,
    create: '/contractors',
    update: (contractorId) => `/contractors/${contractorId}`
  },
  mudPumps: {
    base: '/mud-pumps',
    getByRig: (rigId) => `/mud-pumps/rig/${rigId}`,
    getBySerial: (serialNumber) => `/mud-pumps/serial/${serialNumber}`,
    getByType: (pumpType, rigId) => `/mud-pumps/type/${pumpType}?rigId=${rigId}`,
    create: '/mud-pumps',
    update: (pumpId) => `/mud-pumps/${pumpId}`
  },
  rigEquipments: {
    base: '/rig-equipments',
    getByRig: (rigId) => `/rig-equipments/rig/${rigId}`,
    getByManufacturer: (manufacturer) => `/rig-equipments/manufacturer/${manufacturer}`,
    create: '/rig-equipments',
    update: (equipmentId) => `/rig-equipments/${equipmentId}`
  },
  rigStabilities: {
    base: '/rig-stabilities',
    getByRig: (rigId) => `/rig-stabilities/rig/${rigId}`,
    getByCapacity: (minDeckLoad) => `/rig-stabilities/capacity?minDeckLoad=${minDeckLoad}`,
    create: '/rig-stabilities',
    update: (stabilityId) => `/rig-stabilities/${stabilityId}`
  },
  rigTypes: {
    base: '/rig-types',
    getAll: '/rig-types',
    getById: (rigTypeId) => `/rig-types/${rigTypeId}`,
    create: '/rig-types',
    update: (rigTypeId) => `/rig-types/${rigTypeId}`,
    delete: (rigTypeId) => `/rig-types/${rigTypeId}`
  }
};

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Accept': 'application/json'
  },
  withCredentials: true
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add CORS headers
    config.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000';
    config.headers['Access-Control-Allow-Credentials'] = 'true';

    // Add auth token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Set Content-Type based on data type
    if (config.data instanceof URLSearchParams) {
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else if (typeof config.data === 'object') {
      config.headers['Content-Type'] = 'application/json';
    }

    // Clean up URL if it includes baseURL
    if (config.url.startsWith('/api/v1')) {
      config.url = config.url.substring(7);
    }

    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Ensure we always have response.data
    if (!response.data) {
      console.warn('Empty response data received');
      return {};
    }
    return response.data;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle token expiration
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(
          `${api.defaults.baseURL}${API_ENDPOINTS.auth.refresh}`,
          { refresh_token: refreshToken }
        );

        const { access_token } = response.data;

        if (access_token) {
          localStorage.setItem('token', access_token);
          api.defaults.headers.Authorization = `Bearer ${access_token}`;
          originalRequest.headers.Authorization = `Bearer ${access_token}`;

          return api(originalRequest);
        }
      } catch (refreshError) {
        store.dispatch(logout());
        toast.error('Session expired. Please login again.');
        return Promise.reject(refreshError);
      }
    }

    // Handle other errors
    if (error.response) {
      const message = error.response.data?.detail || 
                     error.response.data?.message || 
                     'An error occurred';
      toast.error(message);
    } else if (error.request) {
      toast.error('Network error. Please check your connection.');
    } else {
      toast.error('An unexpected error occurred.');
    }

    return Promise.reject(error);
  }
);

// Error handling utility
const handleApiError = (error, customMessage = '') => {
  console.error('API Error:', error);

  const errorMessage = error.response?.data?.detail || 
                      error.response?.data?.message ||
                      customMessage ||
                      'An unexpected error occurred';

  toast.error(errorMessage);
  return Promise.reject(new Error(errorMessage));
};

// Single export statement for all exports
export { api as default, handleApiError, API_ENDPOINTS };