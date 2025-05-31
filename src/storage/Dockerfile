FROM python:3.10-slim
WORKDIR /app
COPY upload.py .
RUN pip install fastapi uvicorn minio python-dotenv python-multipart
EXPOSE 9100
CMD ["uvicorn", "upload:app", "--host", "0.0.0.0", "--port", "9100"]
