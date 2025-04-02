FROM python:3.12.3

WORKDIR /app

# Копіюємо файли з локального репозиторію в контейнер
COPY . /app

# Встановлення залежностей з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Встановлення шрифтів
RUN apt-get update && apt-get install -y fonts-dejavu


# Встановлення змінних середовища для шляхи моделей
ENV UPLOAD_DIR=/app/src/materials/pdf
ENV RESULT_DIR=/app/src/materials/txt
ENV CREATED=/app/src/materials/created

# Відкриття порту, на якому працюватиме FastAPI
EXPOSE 8080

# Команда для запуску FastAPI за допомогою uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "src"]