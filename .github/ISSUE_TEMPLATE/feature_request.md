
name: Solicitud de mejora ✨
description: Sugiere una funcionalidad o mejora
title: "[FEATURE] "
labels: [enhancement]
body:
  - type: textarea
    id: summary
    attributes:
      label: ¿Qué te gustaría mejorar?
      placeholder: Explica brevemente la mejora que propones
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Contexto adicional
      placeholder: ¿Por qué es útil? ¿Cómo beneficiaría al proyecto?
