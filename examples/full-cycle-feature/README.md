# Caso semilla — Feature con ciclo completo hasta producción

Caso sintético. Cualquier parecido con un sistema real es coincidencia.

## Situación

Negocio pide un reporte exportable nuevo. No existe el dato agregado, no existe el endpoint, y soporte tendrá que atender preguntas sobre él desde el día uno.

## Quién lo usa / ejecuta

Lo consultan el agente o la persona cuando una solicitud recorre todo el ciclo: diseño, datos, API, soporte y despliegue.

## Orden lógico

```text
1. Analizar y decidir la arquitectura del reporte
2. Implementar la capa de datos
3. Implementar la capa de API
4. Escribir el SOP de soporte
5. Promover entre ambientes en el orden correcto
6. Verificar en la rama de producción
7. Reconciliar cualquier hotfix hacia las ramas activas
```

## Por qué es útil como ejemplo

Muestra un caso donde el orden importa y el error es caro:

- la capa de datos debe desplegarse **antes** que la API que la consume;
- el SOP de soporte no es documentación opcional: sin él, cada duda escala a ingeniería;
- un hotfix aplicado directo en producción debe volver a las ramas activas, o se pierde en el siguiente release.

## Patrón reusable

- arquitectura antes de código;
- una capacidad no basta: el caso activa varias en secuencia;
- el entregable no es solo el código, sino código + guía operativa + orden de despliegue;
- la promoción entre ambientes es un paso con su propio análisis de drift.

## Clasificación esperada

```yaml
primary_capability: architecture_analysis
secondary_capabilities: [implementation, support_sop, environment_promotion]
confidence: 0.85
needs_human_review: true
```

## Capacidades

- `architecture_analysis`;
- `support_sop`;
- `environment_promotion`.

## Preguntas abiertas típicas

- ¿El reporte necesita datos históricos o solo desde su creación?
- ¿Qué volumen tiene la consulta y hace falta paginación o job asíncrono?
- ¿Quién aprueba la ventana de despliegue?
- ¿Qué pasa si la migración de datos falla a medias?
