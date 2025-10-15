import axios from 'axios'

// Типы будут автоматически генерироваться
import type { components } from '@/types/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

const TOKEN_STORAGE_KEY = 'ogorod_market_token'

const authToken = {
  get(): string | null {
    if (typeof window === 'undefined') {
      return null
    }
    return window.localStorage.getItem(TOKEN_STORAGE_KEY)
  },
  set(token: string) {
    if (typeof window === 'undefined') {
      return
    }
    window.localStorage.setItem(TOKEN_STORAGE_KEY, token)
  },
  clear() {
    if (typeof window === 'undefined') {
      return
    }
    window.localStorage.removeItem(TOKEN_STORAGE_KEY)
  },
}

apiClient.interceptors.request.use((config) => {
  const token = authToken.get()
  if (token) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Типизированные методы API
export const api = {
  products: {
    list: () =>
      apiClient.get<components['schemas']['Product'][]>('/products').then(r => r.data),
    
    get: (id: number) => 
      apiClient.get<components['schemas']['Product']>(`/products/${id}`).then(r => r.data),
    
    getBySlug: (slug: string) =>
      apiClient.get<components['schemas']['Product']>(`/products/by-slug/${slug}`).then(r => r.data),
  },
  auth: {
    register: (payload: components['schemas']['UserCreate']) =>
      apiClient.post<components['schemas']['UserRead']>('/auth/register', payload).then(r => r.data),
    login: (payload: components['schemas']['UserLogin']) =>
      apiClient.post<components['schemas']['Token']>('/auth/login', payload).then(r => r.data),
    me: () =>
      apiClient.get<components['schemas']['UserRead']>('/auth/me').then(r => r.data),
  },
}

// Типы для удобства
export type Product = components['schemas']['Product']
export type User = components['schemas']['UserRead']
export type Token = components['schemas']['Token']

export const authStorage = authToken
