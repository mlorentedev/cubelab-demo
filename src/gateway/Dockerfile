FROM python:3.10-slim
WORKDIR /app
COPY main.py .
RUN pip install fastapi uvicorn requests python-dotenv python-multipart
EXPOSE 9200
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9200"]
