# Arquitectura

- **Raspberry Pi**: FastAPI + proxy inverso como punto de entrada
- **Jetson A**: MinIO accesible por red
- **Jetson B**: Proceso de imágenes desde MinIO y creación de thumbnails

## Diagrama

[pendiente añadir diagrama en assets/diagramas/]

## Equivalencias en Cloud

- **MinIO** → Amazon S3
- **FastAPI** → AWS Lambda + API Gateway
- **K3s** → Amazon EKS
- **Jetson GPU** → EC2 con GPU

