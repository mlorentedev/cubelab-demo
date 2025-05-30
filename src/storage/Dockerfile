FROM python:3.10-slim
WORKDIR /app
COPY upload.py .
RUN pip install fastapi uvicorn minio python-dotenv python-multipart
CMD ["uvicorn", "upload:app", "--host", "0.0.0.0", "--port", "9000"]
