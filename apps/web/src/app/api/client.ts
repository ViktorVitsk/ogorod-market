import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Типы будут позже, после генерации из OpenAPI
export interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: number
  unit: string
  image_url?: string
}
