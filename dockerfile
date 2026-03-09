# Используем официальный образ Python
FROM python:3.13-slim

# Копируем код бота
COPY . .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Запускаем бота
ENTRYPOINT ["python", "bot.py"]

