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

// Типизированные методы API
export const api = {
  products: {
    list: () => 
      apiClient.get<components['schemas']['Product'][]>('/products').then(r => r.data),
    
    get: (id: number) => 
      apiClient.get<components['schemas']['Product']>(`/products/${id}`).then(r => r.data),
    
    getBySlug: (slug: string) => 
      apiClient.get<components['schemas']['Product']>(`/products/by-slug/${slug}`).then(r => r.data),
  }
}

// Типы для удобства
export type Product = components['schemas']['Product']