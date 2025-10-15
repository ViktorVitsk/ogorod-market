'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

import { authStorage } from '@/app/api/client'
import { useAuthActions, useCurrentUser } from '@/hooks/useAuth'

export function AuthStatus() {
  const router = useRouter()
  const { data: user, isFetching, isLoading } = useCurrentUser()
  const { logout } = useAuthActions()
  const [hasToken, setHasToken] = useState<boolean>(() => !!authStorage.get())

  useEffect(() => {
    setHasToken(!!authStorage.get())
  }, [])

  useEffect(() => {
    if (user) {
      setHasToken(true)
    }
  }, [user])

  if (hasToken && (isLoading || isFetching) && !user) {
    return (
      <div className="text-sm text-gray-500">
        Проверяем аккаунт...
      </div>
    )
  }

  if (!user) {
    return (
      <div className="flex items-center gap-3 text-sm">
        <Link
          href="/login"
          className="text-green-700 hover:text-green-800 font-medium"
        >
          Войти
        </Link>
        <Link
          href="/register"
          className="text-white bg-green-600 px-3 py-1.5 rounded-md hover:bg-green-700 transition-colors"
        >
          Регистрация
        </Link>
      </div>
    )
  }

  const handleLogout = () => {
    logout()
    setHasToken(false)
    router.push('/login')
  }

  return (
    <div className="flex items-center gap-3 text-sm text-gray-700">
      <span className="font-medium">
        {user.full_name ?? user.email}
      </span>
      <button
        type="button"
        onClick={handleLogout}
        className="text-red-600 hover:text-red-700 transition-colors"
      >
        Выйти
      </button>
    </div>
  )
}
