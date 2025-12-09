FROM python:3.12-slim-bookworm

# Рабочая директория - корень проекта внутри контейнера
WORKDIR /app

# 1. Сначала копируем только requirements (для кэширования слоев Docker)
COPY requirements.txt .

# 2. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 3. ВАЖНО: Копируем код ВНУТРЬ папки api
# Теперь структура будет /app/api/main.py, /app/api/client.py
COPY . ./api

# 4. ВАЖНО: Указываем Python искать модули в /app
ENV PYTHONPATH=/app

# 5. Запускаем как модуль (через -m), а не как файл
CMD ["python", "-m", "api.main"]