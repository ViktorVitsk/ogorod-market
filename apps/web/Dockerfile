FROM node:18-alpine

WORKDIR /app

# Копируем только файлы зависимостей сначала (для кэширования)
COPY package.json pnpm-lock.yaml* ./

# Pin the package manager declared in package.json.
RUN npm install -g pnpm@10.17.1 && pnpm install

# Копируем остальной код
COPY . .

# NEXT_PUBLIC_* is inlined into the browser bundle at build time.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Собираем приложение
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]