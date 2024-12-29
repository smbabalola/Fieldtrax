// src/services/jobCenterService.js
// src/services/jobCenterService.js
import api, { API_ENDPOINTS } from './api';

const jobCenterService = {
  getAll: () => api.get(API_ENDPOINTS.jobCenters.getAll),
  getActive: () => api.get(API_ENDPOINTS.jobCenters.getActive),
  getByWell: (wellName) => api.get(API_ENDPOINTS.jobCenters.getByWell(wellName)),
  getByShortName: (shortName) => api.get(API_ENDPOINTS.jobCenters.getByShortName(shortName)),
  getByCountry: (country) => api.get(API_ENDPOINTS.jobCenters.getByCountry(country)),
  getByDateRange: (startDate, endDate) => api.get(API_ENDPOINTS.jobCenters.getByDateRange(startDate, endDate)),
  create: (data) => api.post(API_ENDPOINTS.jobCenters.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.jobCenters.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.jobCenters.delete(id))
};

export default jobCenterService;