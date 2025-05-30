[![CI](https://github.com/mlorente/cubelab-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/mlorente/cubelab-demo/actions/workflows/ci.yml)

# Homelab Cloud Native

Este proyecto demuestra cómo montar una infraestructura distribuida en casa con una Raspberry Pi 4 y dos Jetson Nano, emulando servicios de AWS como S3, ALB, EC2 y Lambda usando Kubernetes K3s.

## 🚀 Componentes

- **Gateway** (Raspberry Pi 4): API que recibe imágenes
- **Storage** (Jetson Nano A): MinIO emulando S3
- **Procesamiento** (Jetson Nano B): Detección y generación de thumbnails
- **Orquestador**: Kubernetes (K3s)
- **Lenguaje**: Python con FastAPI

## 📚 Documentación

Este repositorio incluye documentación técnica detallada en la carpeta [`docs/`](./docs):

- 📐 [`arquitectura.md`](./docs/arquitectura.md): Diagrama y descripción de la arquitectura distribuida.
- ⚙️ [`instalacion.md`](./docs/instalacion.md): Guía de instalación de dependencias y despliegue.
- 🧪 [`uso.md`](./docs/uso.md): Cómo subir imágenes, verificar resultados y hacer debugging.
- 🛠 [`guia_instalacion.md`](./docs/guia_instalacion.md): Guía paso a paso con hardware y configuraciones.
- ❓ [`faqs.md`](./docs/faqs.md): Preguntas frecuentes sobre configuración, errores comunes y soluciones.

## 📁 Estructura del proyecto

- `src/`: Código fuente de cada servicio
- `scripts/`: Scripts de despliegue
- `docs/`: Documentación extendida
- `assets/`: Diagramas e imágenes

## 🧪 Uso rápido

```bash
curl -X POST -F 'file=@foto.jpg' http://<IP_RPI>:80/upload
```

## 💡 Equivalencias en Cloud

| Homelab         | AWS            |
|-----------------|----------------|
| Raspberry Pi    | ALB            |
| Jetson (MinIO)  | S3             |
| Jetson (CPU)    | Lambda/EC2     |
| K3s             | EKS            |

## 🔁 Desarrollo local paso a paso

Puedes probar todo el sistema en tu propio ordenador sin necesidad de hardware físico.

### ✅ Requisitos

- Python 3.10+
- Docker
- Docker Compose

### 🧪 Instrucciones

```bash
# 1. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verifica o crea el archivo .env
cat .env

# 4. Levanta todo con Docker Compose
docker-compose up --build

# 5. Prueba una imagen
curl -X POST -F 'file=@tests/test.jpg' http://localhost:8080/upload

# 6. Verifica resultados en ./results

# 7. Ejecuta los tests
pytest tests/

# 8. Para limpiar
docker-compose down
deactivate
```

Las miniaturas generadas se almacenan automáticamente en el directorio `./results`, montado desde el contenedor de procesamiento.

## 🐳 Desarrollo local con Docker Compose

Puedes probar toda la arquitectura localmente sin hardware físico:

```bash
docker-compose up --build
```

Esto levanta:
- MinIO en `localhost:9000` (usuario: minio / contraseña: minio123)
- Gateway en `localhost:8080`
- Servicio de almacenamiento conectado a MinIO
- Procesador automático de imágenes en `/results`

Sube una imagen con:

```bash
curl -X POST -F 'file=@foto.jpg' http://localhost:8080/upload
```

## ✅ Pruebas automáticas

Para ejecutar las pruebas de integración locales:

```bash
pip install requests
pytest tests/test_gateway.py
```

Asegúrate de tener `docker-compose up` en ejecución antes de probar.

### 🔬 Cobertura de tests

Además del test de subida, también puedes validar que los thumbnails han sido generados correctamente:

```bash
pytest tests/test_processing.py
```

Puedes generar un reporte de cobertura HTML:

```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
xdg-open htmlcov/index.html  # en Linux
```

## ⚙️ Configuración por entorno (.env)

Este proyecto utiliza un archivo `.env` en la raíz del repositorio para configurar variables sensibles y direcciones IP.

Ejemplo de `.env`:

```env
JETSON_A_HOST=jetson-a
JETSON_B_HOST=jetson-b
RASPBERRY_PI_HOST=raspberry-pi

MINIO_ENDPOINT=http://jetson-a:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123

GATEWAY_PORT=8000
RESULTS_DIR=/results
```

Estas variables son cargadas automáticamente en los servicios mediante `python-dotenv`.

**Importante:** Para probar en local con `docker-compose`, asegúrate de que las IPs o nombres de host se correspondan con los servicios definidos en el archivo `docker-compose.yml`.