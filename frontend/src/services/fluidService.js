// File: /src/services/fluidService.js
import api, { API_ENDPOINTS } from './api';

const fluidService = {
  getByWellbore: (wellboreId) => api.get(API_ENDPOINTS.fluids.getByWellbore(wellboreId)),
  getByType: (wellboreId, fluidType) => api.get(API_ENDPOINTS.fluids.getByType(wellboreId, fluidType)),
  getByDateRange: (startDate, endDate) => api.get(API_ENDPOINTS.fluids.getByDateRange(startDate, endDate)),
  getByCountry: (country) => api.get(API_ENDPOINTS.fluids.getByCountry(country)),
  create: (data) => api.post(API_ENDPOINTS.fluids.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.fluids.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.fluids.delete(id))
};

export default fluidService;