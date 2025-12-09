# Docker Deployment Guide

## Архитектура

```
┌─────────────────────────────────────────────┐
│           Nginx (Port 80/443)               │
│  - Reverse Proxy                            │
│  - /api/* → API Service (8080)              │
│  - /* → Frontend (static)                   │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐       ┌──────────────┐
│ API Service  │◄─────►│ LLM Service  │
│  (Port 8080) │       │  (Port 8081) │
│              │       │  (Internal)  │
└──────────────┘       └──────────────┘
        │
        ▼
┌──────────────┐
│  Frontend    │
│  (Nginx)     │
│  Static      │
└──────────────┘
```

## Сервисы

1. **nginx** - Главный reverse proxy
   - Порты: 80, 443
   - Маршрутизация `/api/*` → API Service
   - Маршрутизация `/*` → Frontend

2. **api** - Backend API (FastAPI)
   - Порт: 8080 (доступен через nginx)
   - Endpoints: `/api/v1/ai/*`

3. **llm** - LLM Service
   - Порт: 8081 (ТОЛЬКО внутри сети контейнеров)
   - Доступ ТОЛЬКО от API сервиса

4. **frontend** - Frontend статика
   - Nginx с собранным Vue.js приложением
   - Доступен через главный nginx

## Быстрый старт

### 1. Настройка переменных окружения

```bash
cp .env.example .env
# Отредактируйте .env и укажите ваши API ключи
```

### 2. Сборка и запуск

```bash
# Сборка всех сервисов
docker-compose build

# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f api
```

### 3. Проверка работы

```bash
# Проверка здоровья API
curl http://localhost/health

# Проверка фронтенда
curl http://localhost/

# Проверка API endpoint
curl -X POST http://localhost/api/v1/ai/generate-ui-tests \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "task": "test"}'
```

## Управление

### Остановка сервисов

```bash
# Остановка
docker-compose stop

# Остановка и удаление контейнеров
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

### Перезапуск отдельного сервиса

```bash
docker-compose restart api
docker-compose restart nginx
docker-compose restart frontend
```

### Просмотр статуса

```bash
docker-compose ps
```

### Логи

```bash
# Все логи
docker-compose logs

# Последние 100 строк с отслеживанием
docker-compose logs --tail=100 -f

# Логи конкретного сервиса
docker-compose logs api
docker-compose logs nginx
```

## Разработка

### Пересборка после изменений

```bash
# Пересборка всех сервисов
docker-compose build

# Пересборка конкретного сервиса
docker-compose build api

# Пересборка без кэша
docker-compose build --no-cache

# Пересборка и перезапуск
docker-compose up -d --build
```

### Доступ к контейнеру

```bash
# Shell в контейнере API
docker-compose exec api sh

# Shell в контейнере Nginx
docker-compose exec nginx sh

# Выполнение команды
docker-compose exec api python -c "import sys; print(sys.version)"
```

## Порты

| Сервис   | Внутренний порт | Внешний порт | Доступ            |
|----------|----------------|--------------|-------------------|
| nginx    | 80, 443        | 80, 443      | Публичный         |
| api      | 8080           | -            | Через nginx       |
| llm      | 8081           | -            | Только от api     |
| frontend | 80             | -            | Через nginx       |

## Безопасность

- LLM сервис доступен ТОЛЬКО внутри Docker сети
- Все внешние запросы идут через Nginx
- API защищен rate limiting в Nginx (опционально)
- HTTPS настраивается через certbot (см. nginx/default.conf)

## Troubleshooting

### Проверка сети

```bash
# Список сетей
docker network ls

# Инспекция сети
docker network inspect testops-copilot_testops-network
```

### Проверка подключения между контейнерами

```bash
# Из api к llm
docker-compose exec api ping llm

# Проверка доступности LLM из API
docker-compose exec api curl http://llm:8081/api/v1/ai/health
```

### Очистка

```bash
# Удалить все остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune

# Полная очистка
docker system prune -a
```

## Production Deployment

### HTTPS с Let's Encrypt

Раскомментируйте HTTPS блок в `nginx/default.conf` и настройте certbot:

```bash
# Установка certbot
apt-get install certbot python3-certbot-nginx

# Получение сертификата
certbot --nginx -d testops-cloud.ru
```

### Мониторинг

```bash
# Добавьте в docker-compose.yaml:
# prometheus, grafana для мониторинга
# loki для централизованных логов
```

### Автоматические обновления

```bash
# Создайте systemd service для автоматического запуска
sudo systemctl enable docker-compose@testops
```
