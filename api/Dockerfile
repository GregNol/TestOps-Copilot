FROM python:3.12-slim-bookworm

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей (если нужны для сборки некоторых питон пакетов)
# RUN apt-get update && apt-get install -y gcc

# Копирование requirements
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода приложения
COPY . .
# Создание папки ресурсов, если она не скопировалась (хотя COPY . . скопирует её)
# Убедитесь, что resources/prompt_template.txt существует

# Запуск
CMD ["python", "main.py"]