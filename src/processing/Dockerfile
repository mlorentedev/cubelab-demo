FROM python:3.10-slim
WORKDIR /app
COPY main.py .
RUN pip install python-dotenv fastapi uvicorn minio opencv-python-headless
EXPOSE 9300
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9300"]
