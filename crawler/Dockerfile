# crawler/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY crawler.py .
COPY leak_sample.txt .

RUN pip install --no-cache-dir requests

CMD ["python", "crawler.py"]
