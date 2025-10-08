import type { Metadata } from 'next'
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
      <body className="antialiased">
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  )
}