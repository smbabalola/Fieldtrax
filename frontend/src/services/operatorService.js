import api, { API_ENDPOINTS } from './api';

const operatorService = {
  getAll: () => api.get(API_ENDPOINTS.operators.getAll),
  getByName: (name) => api.get(API_ENDPOINTS.operators.getByName(name)),
  getByCode: (code) => api.get(API_ENDPOINTS.operators.getByCode(code)),
  create: (data) => api.post(API_ENDPOINTS.operators.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.operators.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.operators.delete(id))
};

export default operatorService;