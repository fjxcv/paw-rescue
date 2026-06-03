import api from './index';

export const adoptAPI = {
  getAll: () => api.get('/adopt/applications/'),
  create: (data) => api.post('/adopt/applications/', data),
  getMy: () => api.get('/adopt/applications/my/'),
  submitQuestionnaire: (id, answers_json) => api.post(`/adopt/applications/${id}/questionnaire/`, { answers_json }),
  addAttachment: (id, data) => api.post(`/adopt/applications/${id}/attachments/`, data),
  audit: (id, data) => api.put(`/adopt/applications/${id}/audit/`, data),
  offlineVerify: (id, data) => api.put(`/adopt/offline-verify/${id}/`, data),
};
