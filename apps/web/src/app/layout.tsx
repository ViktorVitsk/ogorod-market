import type { Metadata } from 'next'

import { AuthStatus } from '@/components/AuthStatus'

import { QueryProvider } from './QueryProvider'
import './globals.css'

export const metadata: Metadata = {
  title: 'Огород Маркет - Свежие овощи',
  description: 'Натуральные продукты от местных фермеров',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className="antialiased bg-green-50 min-h-screen">
        <QueryProvider>
          <header className="bg-white shadow-sm">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
              <h1 className="text-2xl font-bold text-green-800">
                <a href="/">Огород Маркет</a>
              </h1>
              <AuthStatus />
            </div>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
        </QueryProvider>
      </body>
    </html>
  )
}
