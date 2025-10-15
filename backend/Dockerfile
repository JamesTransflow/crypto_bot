FROM python:3.13-slim

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONPATH=/backend

# Expose the port
EXPOSE 8000

# Run the application (main.py is in app/ directory)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]