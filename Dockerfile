FROM python:3.12.0-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY check_numeric.py .
COPY check_rules.py .
COPY README.md .
COPY styles.css .
COPY /sensitive-header ./sensitive-header
COPY /sensitive-content ./sensitive-content
RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8000
EXPOSE $PORT
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]