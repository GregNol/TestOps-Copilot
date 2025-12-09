FROM nginx:1.25-alpine

# Устанавливаем необходимые пакеты
RUN apk update && \
    apk add --no-cache \
    brotli \
    nginx-mod-http-brotli \
    && rm -rf /var/cache/apk/*

# Копируем конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/http.d/default.conf

# Создаем директории для логов
RUN mkdir -p /var/log/nginx

# Открываем порты
EXPOSE 80 443

# Запускаем Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]
