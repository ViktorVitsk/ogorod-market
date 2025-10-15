'use client'

import { useCallback } from 'react'
import {
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query'

import { api, authStorage } from '@/app/api/client'

export function useCurrentUser() {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: () => api.auth.me(),
    enabled: typeof window !== 'undefined' && !!authStorage.get(),
    retry: false,
  })
}

export function useAuthActions() {
  const queryClient = useQueryClient()

  const loginMutation = useMutation({
    mutationFn: api.auth.login,
    onSuccess: (token) => {
      authStorage.set(token.access_token)
      queryClient.invalidateQueries({ queryKey: ['auth'] })
    },
  })

  const registerMutation = useMutation({
    mutationFn: api.auth.register,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] })
    },
  })

  const logout = useCallback(() => {
    authStorage.clear()
    queryClient.setQueryData(['auth', 'me'], null)
    queryClient.removeQueries({ queryKey: ['auth', 'me'] })
  }, [queryClient])

  return {
    loginMutation,
    registerMutation,
    logout,
  }
}
