FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY templates/ ./templates/
COPY css/ ./static/css/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]