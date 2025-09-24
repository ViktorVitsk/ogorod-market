FROM node:18-alpine

WORKDIR /app

# Копируем только файлы зависимостей сначала (для кэширования)
COPY package.json pnpm-lock.yaml* ./

# Устанавливаем pnpm
RUN npm install -g pnpm && pnpm install

# Копируем остальной код
COPY . .

# Собираем приложение
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]