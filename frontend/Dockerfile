FROM node:20-alpine AS builder

WORKDIR /app

# Копируем package files
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходники
COPY frontend/ ./

# Собираем production build
RUN npm run build

# Production stage - Nginx для отдачи статики
FROM nginx:1.25-alpine

# Удаляем дефолтную конфигурацию
RUN rm -rf /usr/share/nginx/html/*

# Копируем собранное приложение
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфигурацию Nginx для фронтенда
COPY frontend/nginx/default.conf /etc/nginx/conf.d/default.conf

# Открываем порт
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]