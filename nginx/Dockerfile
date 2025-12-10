FROM nginx:1.25-alpine

# Устанавливаем Nginx без дополнительных модулей, чтобы избежать несовместимостей
RUN apk update && \
    apk add --no-cache nginx && \
    rm -f /etc/nginx/conf.d/default.conf && \
    rm -rf /etc/nginx/modules/*.conf /var/cache/apk/*

# Копируем конфигурацию
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/http.d/default.conf

# Создаем директории для логов
RUN mkdir -p /var/log/nginx

# Открываем порты
EXPOSE 80 443

# Запускаем Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]
