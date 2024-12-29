import api, { API_ENDPOINTS } from './api';

const contractorService = {
  getByName: (name) => api.get(API_ENDPOINTS.contractors.getByName(name)),
  getByCountry: (country) => api.get(API_ENDPOINTS.contractors.getByCountry(country)),
  getByDateRange: (startDate, endDate) => api.get(API_ENDPOINTS.contractors.getByDateRange(startDate, endDate)),
  getByType: (type) => api.get(API_ENDPOINTS.contractors.getByType(type)),
  create: (data) => api.post(API_ENDPOINTS.contractors.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.contractors.update(id), data),
  getById: (id) => api.get(API_ENDPOINTS.contractors.getById(id)),
  delete: (id) => api.delete(API_ENDPOINTS.contractors.delete(id))
};

export default contractorService;
