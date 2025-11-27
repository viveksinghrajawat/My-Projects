FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn psycopg2
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
