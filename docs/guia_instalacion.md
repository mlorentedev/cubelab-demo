
# Guía de Instalación Homelab Cloud Native

## 🧰 Hardware necesario

| Componente             | Cantidad | Precio aprox. (€) |
|------------------------|----------|-------------------|
| Raspberry Pi 4 (4GB)   | 1        | 60                |
| NVIDIA Jetson Nano     | 2        | 70 x 2 = 140      |
| Tarjetas microSD (32GB)| 3        | 10 x 3 = 30       |
| SSD o pendrive rápido  | 1        | 20                |
| Switch/Router Ethernet | 1        | Ya disponible     |
| Fuente alimentación    | 3        | Ya disponible     |

**Total estimado:** ~200 €

## 🖥️ Paso 1: Preparar Raspberry Pi

1. Descargar Raspberry Pi OS Lite desde raspberrypi.com
2. Flashea con Raspberry Pi Imager
3. Habilita SSH creando archivo vacío 'ssh'
4. Inserta SD y arranca la Raspberry Pi
5. Accede por SSH y actualiza el sistema

## 🧠 Paso 2: Preparar Jetson Nano

1. Descarga JetPack desde developer.nvidia.com
2. Flashea SD con balenaEtcher
3. Enciende, configura y activa modo rendimiento
4. Instala dependencias

## 🌐 Paso 3: Configurar Red

- IPs estáticas recomendadas
- Todos los dispositivos en misma red
- Verifica con ping

## ⚙️ Paso 4: Instalar K3s

En Raspberry Pi:
```
curl -sfL https://get.k3s.io | sh -
```

En Jetson Nano:
```
curl -sfL https://get.k3s.io | K3S_URL=https://<ip-master>:6443 K3S_TOKEN=<token> sh -
```

## 🚀 Paso 5: Desplegar servicios

```
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 🧪 Paso 6: Probar

```
curl -X POST -F 'file=@foto.jpg' http://<ip-gateway>/upload
```
