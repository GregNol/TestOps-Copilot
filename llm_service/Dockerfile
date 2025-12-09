FROM python:3.12-slim-bookworm

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода приложения
COPY . .

# Переменная окружения для порта (по умолчанию 8080)
ENV PORT=8080

# Открываем порт
EXPOSE ${PORT}

# Запуск
CMD ["python", "main.py"]