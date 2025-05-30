
# Makefile para CubeLab Demo

APP_NAMES = gateway storage processing

.PHONY: all build up down logs test venv init clean kube-deploy kube-logs kube-clean

# === LOCAL DEV ===

build:              ## Construye imágenes Docker
	docker compose build

up:                 ## Arranca servicios con Docker Compose
	docker compose up --build

down:               ## Detiene servicios locales
	docker compose down

logs:               ## Muestra logs de docker-compose
	docker compose logs --follow

venv:               ## Crea entorno virtual
	python3 -m venv .venv
	. .venv/bin/activate

init:               ## Instala dependencias y congela en requirements.txt
	. .venv/bin/activate && pip install python-dotenv requests pytest opencv-python-headless minio fastapi uvicorn && pip freeze > requirements.txt
	. .venv/bin/activate && pip install -r requirements.txt

test:               ## Ejecuta pruebas desde entorno virtual
	. .venv/bin/activate && pytest tests/

clean:              ## Limpia entorno local
	docker compose down -v
	rm -rf .venv __pycache__ htmlcov .pytest_cache

# === ENTORNO KUBERNETES ===

kube-deploy:        ## Aplica manifiestos K8s
	kubectl apply -f src/k8s/deployments.yaml

kube-logs:          ## Muestra logs de pods en K8s
	kubectl logs -l app=gateway --tail=50
	kubectl logs -l app=storage --tail=50
	kubectl logs -l app=processing --tail=50

kube-clean:         ## Elimina recursos K8s
	kubectl delete -f src/k8s/deployments.yaml