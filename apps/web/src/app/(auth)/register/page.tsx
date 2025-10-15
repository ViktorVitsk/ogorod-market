'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { useAuthActions } from '@/hooks/useAuth'

export default function RegisterPage() {
  const router = useRouter()
  const { registerMutation } = useAuthActions()
  const [email, setEmail] = useState('')
  const [fullName, setFullName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    try {
      await registerMutation.mutateAsync({ email, password, full_name: fullName || undefined })
      router.push('/login')
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8 border border-green-100">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Регистрация
        </h1>

        {error ? (
          <p className="mb-4 text-sm text-red-600 text-center">
            {error}
          </p>
        ) : null}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:ring-2 focus:ring-green-200 outline-none"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
              Имя (необязательно)
            </label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:ring-2 focus:ring-green-200 outline-none"
              placeholder="Иван Иванов"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Пароль
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
              minLength={8}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-green-500 focus:ring-2 focus:ring-green-200 outline-none"
              placeholder="Не менее 8 символов"
            />
          </div>

          <button
            type="submit"
            disabled={registerMutation.isPending}
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {registerMutation.isPending ? 'Создаем...' : 'Зарегистрироваться'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Уже есть аккаунт?{' '}
          <Link href="/login" className="text-green-600 hover:underline">
            Войти
          </Link>
        </p>
      </div>
    </div>
  )
}
