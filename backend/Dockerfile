FROM python:3.10

WORKDIR /app

# Copy only requirements to build dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Do NOT copy source code here — it will be mounted as volume

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
