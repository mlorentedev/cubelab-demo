
# FAQs - Preguntas frecuentes

## ¿Qué sistema operativo debo usar?

- Raspberry Pi: Raspberry Pi OS Lite (64-bit)
- Jetson Nano: JetPack 4.6 (basado en Ubuntu 18.04)

## ¿Puedo usar Wi-Fi?

Sí, pero se recomienda red cableada por estabilidad.

## ¿Qué pasa si K3s no detecta nodos?

- Verifica IP del master y el token.
- Asegúrate de que no haya firewalls bloqueando el puerto 6443.

## ¿Dónde se guardan los thumbnails?

En Jetson B, ruta `/results`. Puedes montar volumen o exportarlo.

## ¿Puedo extender el sistema?

Sí, puedes añadir más nodos Jetson, balanceadores avanzados (Traefik), y autenticación con Keycloak.
