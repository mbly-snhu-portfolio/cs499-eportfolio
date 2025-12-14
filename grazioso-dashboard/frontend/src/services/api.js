/**
 * API client service for backend communication.
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear storage and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '#/app/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await apiClient.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  logout: async () => {
    await apiClient.post('/api/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/auth/me');
    return response.data;
  },
};

// Animals API
export const animalsAPI = {
  list: async (params = {}) => {
    const response = await apiClient.get('/api/animals', { params });
    return response.data;
  },
  
  get: async (animalId) => {
    const response = await apiClient.get(`/api/animals/${animalId}`);
    return response.data;
  },
  
  create: async (animalData) => {
    const response = await apiClient.post('/api/animals', animalData);
    return response.data;
  },
  
  update: async (animalId, animalData) => {
    const response = await apiClient.put(`/api/animals/${animalId}`, animalData);
    return response.data;
  },
  
  delete: async (animalId) => {
    await apiClient.delete(`/api/animals/${animalId}`);
  },
};

// Analytics API
export const analyticsAPI = {
  getBreedAnalytics: async (params = {}) => {
    const response = await apiClient.get('/api/analytics/breeds', { params });
    return response.data;
  },
};

// Health check
export const healthAPI = {
  check: async () => {
    const response = await apiClient.get('/api/health');
    return response.data;
  },
};

export default apiClient;

