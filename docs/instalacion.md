# Instalación del Homelab

1. Flashea Raspberry Pi OS Lite en la Raspberry Pi 4.
2. Flashea JetPack en ambas Jetson Nano.
3. Conecta Jetson A con SSD USB como almacenamiento.
4. Configura red local con IPs estáticas si es posible.
5. Instala K3s en Raspberry Pi como nodo maestro:
```bash
curl -sfL https://get.k3s.io | sh -
```
6. Une las Jetson como nodos:
```bash
K3S_URL=https://<master-ip>:6443 K3S_TOKEN=<token> sh -s - agent
```
7. Ejecuta `deploy.sh` para desplegar todos los pods.
