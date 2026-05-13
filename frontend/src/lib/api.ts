import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('learnfun_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('learnfun_token');
      if (!window.location.pathname.startsWith('/auth')) {
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email: string, password: string) => api.post('/auth/login', { email, password }),
  register: (name: string, email: string, password: string, grade: string, avatar?: string) =>
    api.post('/auth/register', { name, email, password, grade, avatar }),
  googleLogin: (googleData: any) => api.post('/auth/google', googleData),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data: any) => api.put('/auth/profile', data),
};

export const quizzesAPI = {
  getAll: (params?: any) => api.get('/quizzes', { params }),
  getById: (id: string) => api.get(`/quizzes/${id}`),
  submit: (id: string, answers: any) => api.post(`/quizzes/${id}/submit`, { answers }),
  getScores: () => api.get('/quizzes/scores'),
  getLeaderboard: () => api.get('/quizzes/leaderboard'),
};

export const lessonsAPI = {
  getAll: (params?: any) => api.get('/lessons', { params }),
  getById: (id: string) => api.get(`/lessons/${id}`),
  complete: (id: string) => api.post(`/lessons/${id}/complete`),
  getProgress: () => api.get('/lessons/progress'),
};

export const analyticsAPI = {
  getStats: () => api.get('/analytics/stats'),
  getWeakAreas: () => api.get('/analytics/weak-areas'),
  getRecommendations: () => api.get('/analytics/recommendations'),
};

export const aiAPI = {
  chat: (message: string, context?: any) => api.post('/ai/chat', { message, context }),
  getHelp: (quizId: string, questionIndex: number) =>
    api.post('/ai/help', { quizId, questionIndex }),
};

export default api;
