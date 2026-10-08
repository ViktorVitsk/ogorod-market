'use client'

import { useProducts } from '@/hooks/useProducts'

export default function CatalogPage() {
  const { data: products, isLoading, error } = useProducts()

  if (isLoading) {
    return <div className="text-center">Загрузка товаров...</div>
  }

  if (error) {
    return (
      <div className="text-center text-red-600">
        Ошибка загрузки товаров: {(error as Error).message}
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-green-800 mb-8">
        Каталог товаров
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products?.map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h2 className="text-xl font-semibold text-green-700 mb-2">
              {product.name}
            </h2>
            <p className="text-gray-600 mb-4 line-clamp-2">
              {product.description}
            </p>
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold text-green-600">
                {product.price} ₽
                <span className="text-sm text-gray-500">/{product.unit}</span>
              </span>
              <button
                type="button"
                disabled
                title="Добавление в корзину на сайте ещё не подключено"
                className="bg-green-500 text-white px-4 py-2 rounded disabled:cursor-not-allowed disabled:opacity-60"
              >
                В корзину
              </button>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              В наличии: {product.stock_quantity} {product.unit}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
