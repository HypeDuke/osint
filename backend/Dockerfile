# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy psycopg2-binary \
    python-multipart pydantic passlib[bcrypt] redis requests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
