import { useQuery } from '@tanstack/react-query'
import { api } from '@/app/api/client'

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => api.products.list(),
  })
}

export const useProduct = (id: number) => {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => api.products.get(id),
    enabled: !!id,
  })
}

export const useProductBySlug = (slug: string) => {
  return useQuery({
    queryKey: ['product', slug],
    queryFn: () => api.products.getBySlug(slug),
    enabled: !!slug,
  })
}
