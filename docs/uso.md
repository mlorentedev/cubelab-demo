# Uso de la Aplicación

1. Envía una imagen al endpoint de la Raspberry Pi:
```bash
curl -X POST -F 'file=@foto.jpg' http://<gateway-ip>/upload
```
2. La imagen se sube a MinIO (Jetson A)
3. Jetson B detecta la imagen y crea un thumbnail
4. Puedes consultar `/results/` o extender el sistema para servirlas
