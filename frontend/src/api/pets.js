import api from './index';

export const uploadAPI = {
  upload: (file, subdir = 'uploads') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('subdir', subdir);
    return api.post('/uploads/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const petsAPI = {
  getAll: (params) => api.get('/pets/', { params }),
  getById: (id) => api.get(`/pets/${id}/`),
  create: (data) => api.post('/pets/', data),
  update: (id, data) => api.patch(`/pets/${id}/`, data),
  delete: (id) => api.delete(`/pets/${id}/`),
  getMyPets: () => api.get('/pets/my/'),
};

export const rescueAPI = {
  getAll: () => api.get('/rescue/cases/'),
  getById: (id) => api.get(`/rescue/cases/${id}/`),
  create: (data) => api.post('/rescue/cases/', data),
  updateStatus: (id, data) => api.patch(`/rescue/cases/${id}/status/`, data),
};
