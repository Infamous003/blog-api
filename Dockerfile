FROM python:bookworm

COPY routes /app/routes
COPY app.py /app/
COPY database.py /app/
COPY models.py /app/
COPY utils.py /app/
COPY requirements.txt /app/

WORKDIR /app

ENV PYTHONPATH=/app
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=password123
ENV DB_NAME=blogapi
ENV HOST=postgres
ENV PORT=5432

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379


RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]