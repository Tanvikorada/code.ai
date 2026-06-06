import axios from 'axios'

const API_BASE_URL = 'https://codexatlas-backend.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface RepositoryData {
  url: string
}

export interface ParsedRepository {
  id: string
  name: string
  url: string
  framework: string
  language: string
  files: any[]
  nodes: any[]
  edges: any[]
  health?: any
}

export const apiService = {
  // Auth
  async login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', username); // Form data requires 'username'
    formData.append('password', password);
    const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  async register(username: string, password: string, email: string) {
    const response = await api.post('/api/auth/register', { email: email || username, password });
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },

  // Scan & Polling
  async scanRepository(url: string, onProgress?: (status: string) => void): Promise<ParsedRepository> {
    const response = await api.post('/api/github/scan', { url })
    const { id } = response.data

    // Poll for status
    while (true) {
      await new Promise(resolve => setTimeout(resolve, 3000)) // Poll every 3s
      const statusRes = await api.get(`/api/github/status/${id}`)
      const status = statusRes.data.status
      if (onProgress) onProgress(status)
      if (status === 'completed') {
        const resultRes = await api.get(`/api/github/result/${id}`)
        const data = resultRes.data
        return {
          id,
          name: data.metadata?.name || statusRes.data.url.split('/').pop().replace('.git', ''),
          url: data.metadata?.url || statusRes.data.url,
          framework: data.metadata?.framework || 'unknown',
          language: data.metadata?.language || 'unknown',
          files: [],
          nodes: data.graph?.nodes || [],
          edges: data.graph?.edges || [],
          health: data.health || null
        }
      }
      if (status === 'failed') {
        throw new Error('Scan failed')
      }
    }
  },

  async getGraph(repoId: string): Promise<{ nodes: any[]; edges: any[] }> {
    const response = await api.get(`/api/graph/${repoId}`)
    return response.data
  },

  async getArchitecture(repoId: string): Promise<any> {
    const response = await api.get(`/api/architecture/${repoId}`)
    return response.data
  },

  async getDependencies(repoId: string): Promise<any> {
    const response = await api.get(`/api/dependencies/${repoId}`)
    return response.data
  },

  async generateDocumentation(repoId: string): Promise<any> {
    const response = await api.post(`/api/documentation/generate`, { repoId })
    return response.data
  },

  async analyzeHealth(repoId: string): Promise<any> {
    const response = await api.get(`/api/health/${repoId}`)
    return response.data
  },

  async askAI(repoId: string, question: string, customApiKey?: string): Promise<any> {
    const headers: any = {}
    if (customApiKey) {
      headers['X-Custom-API-Key'] = customApiKey
    }
    const response = await api.post('/api/ai/ask', { repoId, question }, { headers })
    return response.data
  },
}

export default api
