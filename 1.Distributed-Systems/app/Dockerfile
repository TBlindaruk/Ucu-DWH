FROM python:3.9-slim

WORKDIR /app

# Копіюємо файли requirements.txt та ваш код
COPY requirements.txt .
COPY app.py .

COPY .. .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт
EXPOSE 5000

# Запускаємо сервер
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]