
name: Informe de error 🐛
description: Reporta un bug para mejorar el proyecto
title: "[BUG] "
labels: [bug]
body:
  - type: textarea
    id: describe
    attributes:
      label: Describe el problema
      placeholder: Qué está fallando, pasos para reproducirlo...
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Versión usada (código/imagen)
      placeholder: Ej. gateway:latest
  - type: textarea
    id: logs
    attributes:
      label: Logs relevantes
      placeholder: Pega aquí cualquier error o salida del sistema
