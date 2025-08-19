FROM python:3.13-slim

WORKDIR /app

COPY api_llm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_llm /app/api_llm
COPY llm /app/llm

ENV PYTHONPATH=/app

CMD ["uvicorn", "api_llm.main:app", "--host", "0.0.0.0", "--port", "8001"]
