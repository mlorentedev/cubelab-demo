#!/bin/bash
set -e
echo "Desplegando servicios..."
kubectl apply -f src/k8s/deployments.yaml
echo "Todos los servicios fueron desplegados correctamente."
