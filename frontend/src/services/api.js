import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchApi = {
  search: async (query, modelIds, numResults = 5) => {
    try {
      const response = await api.post('/search', {
        query,
        ai_model_ids: modelIds,
        num_results: numResults,
      });
      return response.data;
    } catch (error) {
      console.error('Search error:', error);
      throw error;
    }
  },
  
  getModels: async () => {
    try {
      const response = await api.get('/models');
      return response.data;
    } catch (error) {
      console.error('Get models error:', error);
      throw error;
    }
  },
};

export default api; 