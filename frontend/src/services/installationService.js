import api, { API_ENDPOINTS } from './api';

const installationService = {
  getByField: (fieldId) => api.get(API_ENDPOINTS.installations.getByField(fieldId)),
  getByType: (typeId) => api.get(API_ENDPOINTS.installations.getByType(typeId)),
  getByDateRange: (startDate, endDate) => api.get(API_ENDPOINTS.installations.getByDateRange(startDate, endDate)),
  getByCountry: (country) => api.get(API_ENDPOINTS.installations.getByCountry(country)),
  create: (data) => api.post(API_ENDPOINTS.installations.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.installations.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.installations.delete(id))
};

export default installationService;
