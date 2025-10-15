import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="text-center">
      <h2 className="text-4xl font-bold text-green-700 mb-6">
        Свежие овощи прямо с грядки
      </h2>
      <p className="text-lg text-gray-600 mb-8">
        Натуральные продукты от местных фермеров
      </p>

      <Link
        href="/catalog"
        className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
      >
        Смотреть каталог
      </Link>
    </div>
  )
}
