FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/api_auth

CMD ["uvicorn", "api_auth.main:app", "--host", "0.0.0.0", "--port", "8000"]
