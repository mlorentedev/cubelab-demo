[![CI](https://github.com/mlorente/cubelab-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/mlorente/cubelab-demo/actions/workflows/ci.yml)

# CubeLab Demo - Homelab Cloud Native

Este proyecto demuestra cómo construir una infraestructura distribuida en casa usando una Raspberry Pi 4 y dos Jetson Nano, emulando servicios cloud como S3, API Gateway y procesamiento de imágenes usando Kubernetes (K3s).

## Arquitectura del Sistema

El proyecto simula una arquitectura de microservicios distribuida con tres nodos principales:

- **Gateway** (Raspberry Pi): Punto de entrada API que recibe uploads
- **Storage** (Jetson A): MinIO como almacenamiento compatible con S3
- **Processing** (Jetson B): Procesamiento automático de imágenes y generación de thumbnails
- **Orquestación**: Kubernetes (K3s) para la gestión de contenedores

## Componentes Técnicos

| Servicio | Tecnología | Puerto | Función |
|----------|------------|--------|---------|
| Gateway | FastAPI + Python | 9200 | API de entrada y proxy |
| Storage | MinIO + FastAPI | 9100 | Almacenamiento de objetos |
| Processing | OpenCV + Python | 9300 | Procesamiento de imágenes |
| MinIO Console | MinIO | 9000/9001 | Dashboard de almacenamiento |

## Documentación Completa

La documentación técnica detallada está disponible en [`docs/`](./docs):

- [**Arquitectura**](./docs/arquitectura.md): Diagrama y descripción de componentes
- [**Guía de Instalación**](./docs/guia_instalacion.md): Hardware requerido y configuración paso a paso
- [**Instalación Técnica**](./docs/instalacion.md): Despliegue en K3s y configuración
- [**Manual de Uso**](./docs/uso.md): Cómo subir imágenes y verificar resultados
- [**FAQs**](./docs/faqs.md): Solución a problemas comunes

## Hardware Requerido

| Componente | Cantidad | Función |
|------------|----------|---------|
| Raspberry Pi 4 (4GB+) | 1 | Nodo maestro K3s + Gateway |
| NVIDIA Jetson Nano | 2 | Nodos worker (storage + processing) |
| MicroSD (32GB+) | 3 | Sistema operativo |
| SSD/USB Storage | 1 | Almacenamiento MinIO |
| Switch Ethernet | 1 | Red local |

**Costo estimado:** ~200€

## Equivalencias Cloud

| Homelab Component | AWS Equivalent | Azure Equivalent |
|-------------------|----------------|------------------|
| Raspberry Pi Gateway | API Gateway + ALB | Application Gateway |
| Jetson + MinIO | S3 + EC2 | Blob Storage + VM |
| Jetson Processing | Lambda + EC2 GPU | Functions + GPU VM |
| K3s Cluster | EKS | AKS |

## Desarrollo Local

### Prerrequisitos

- **Python 3.10+**
- **Docker & Docker Compose**
- **Git**

### Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/mlorente/cubelab-demo.git
cd cubelab-demo

# 2. Configurar entorno
cp .env.example .env
# Editar .env con tus configuraciones si es necesario

# 3. Crear entorno virtual Python
make venv
source .venv/bin/activate

# 4. Instalar dependencias
make init

# 5. Levantar todos los servicios
make up

# 6. Probar el sistema
curl -X POST -F 'file=@tests/test.jpg' http://localhost:8080/upload

# 7. Verificar thumbnails generados
ls -la results/

# 8. Ejecutar tests
make test
```

### Servicios Locales

Una vez ejecutado `make up`, tendrás disponible:

| Servicio | URL Local | Credenciales |
|----------|-----------|--------------|
| Gateway API | http://localhost:8080 | - |
| MinIO Console | http://localhost:9001 | minio / minio123 |
| MinIO API | http://localhost:9000 | - |
| Storage Service | http://localhost:9100 | - |
| Processing Service | http://localhost:8001 | - |

### Workflow de Procesamiento

1. **Upload**: Cliente sube imagen → Gateway (puerto 8080)
2. **Storage**: Gateway reenvía → Storage service → MinIO bucket
3. **Processing**: Servicio detecta nueva imagen → Descarga → Crea thumbnail
4. **Results**: Thumbnail guardado en `./results/thumb_[filename].jpg`

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

Las principales variables configurables están en [`.env.example`](.env.example):

```bash
# Hosts de dispositivos físicos
JETSON_A_HOST=jetson-a          # Nodo de almacenamiento
JETSON_B_HOST=jetson-b          # Nodo de procesamiento
RASPBERRY_PI_HOST=raspberry-pi   # Nodo gateway

# Configuración MinIO
BUCKET_NAME=images
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123

# Configuración de servicios
STORAGE_UPLOAD_URL=http://storage:9100/upload
RESULTS_DIR=/results
SCAN_INTERVAL=30                 # Segundos entre escaneos
```

### Testing y CI/CD

```bash
# Tests unitarios
pytest tests/test_gateway.py
pytest tests/test_processing.py

# Test de integración completo
pytest tests/ -v

# Cobertura de código
pip install pytest-cov
pytest --cov=src --cov-report=html
```

El pipeline de CI en [`.github/workflows/ci.yml`](.github/workflows/ci.yml) ejecuta automáticamente tests en cada push y pull request.

## Despliegue en Homelab

### K3s en Raspberry Pi (Master)

```bash
curl -sfL https://get.k3s.io | sh -
```

### Jetson Nano como Workers

```bash
# Obtener token del master
sudo cat /var/lib/rancher/k3s/server/node-token

# En cada Jetson
curl -sfL https://get.k3s.io | K3S_URL=https://<IP_RASPBERRY>:6443 K3S_TOKEN=<TOKEN> sh -s - agent
```

### Despliegue de Aplicación

```bash
# Aplicar manifiestos K8s
make kube-deploy

# Verificar pods
kubectl get pods -o wide

# Ver logs
make kube-logs
```

## Estructura del Proyecto

```text
cubelab-demo/
├── src/
│   ├── gateway/         # API Gateway (Raspberry Pi)
│   ├── storage/         # MinIO storage service (Jetson A)
│   ├── processing/      # Image processing (Jetson B)
│   └── k8s/            # Manifiestos Kubernetes
├── docs/               # Documentación técnica
├── tests/              # Tests automatizados
├── scripts/            # Scripts de despliegue
├── .github/            # CI/CD workflows
├── docker-compose.yml  # Desarrollo local
├── Makefile           # Comandos automatizados
└── requirements.txt   # Dependencias Python
```

## Contribuir

Por favor revisa [CONTRIBUTING.md](CONTRIBUTING.md) para:

- Guías de estilo de código
- Proceso de pull requests
- Plantillas de issues

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## Soporte

- **Documentación**: [`docs/`](./docs)
- **Reportar bugs**: [GitHub Issues](https://github.com/mlorente/cubelab-demo/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/mlorente/cubelab-demo/discussions)
- **FAQs**: [`docs/faqs.md`](./docs/faqs.md)
