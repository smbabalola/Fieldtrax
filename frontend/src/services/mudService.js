import api, { API_ENDPOINTS } from './api';

const mudService = {
  getEquipmentByReport: (reportId) => api.get(API_ENDPOINTS.mudEquipmentDetails.getByReport(reportId)),
  createEquipment: (data) => api.post(API_ENDPOINTS.mudEquipmentDetails.create, data),
  updateEquipment: (id, data) => api.put(API_ENDPOINTS.mudEquipmentDetails.update(id), data),
  getPumpByReport: (reportId) => api.get(API_ENDPOINTS.mudPumpDetails.getByReport(reportId)),
  getActivePumps: async (reportId) => {
    const response = await api.get(`/mud-pumps/report/${reportId}/active`);
    return response.data;
  },
  createPump: (data) => api.post(API_ENDPOINTS.mudPumpDetails.create, data),
  updatePump: (id, data) => api.put(API_ENDPOINTS.mudPumpDetails.update(id), data),
  getByReport: (reportId) => api.get(API_ENDPOINTS.mudEquipment.getByReport(reportId)),
  create: (data) => api.post(API_ENDPOINTS.mudEquipment.create, data),
  update: (id, data) => api.put(API_ENDPOINTS.mudEquipment.update(id), data),
  delete: (id) => api.delete(API_ENDPOINTS.mudEquipment.delete(id))
};

export default mudService;