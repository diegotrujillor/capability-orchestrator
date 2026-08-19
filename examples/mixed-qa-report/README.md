# Caso semilla — Reporte de QA con frentes mezclados

Caso sintético. Cualquier parecido con un sistema real es coincidencia.

## Situación

Llega un mensaje de QA con tres quejas en un solo párrafo:

```text
"El listado no carga después de filtrar, además el total de la pantalla de resumen
no cuadra con el detalle, y el correo de confirmación llega sin el adjunto.
Todo empezó ayer."
```

## Quién lo usa / ejecuta

Lo consultan el agente o la persona cuando una nueva solicitud mezcla síntomas de módulos distintos.

## Orden lógico

```text
1. Leer input original
2. Separar frentes funcionales
3. Confirmar hechos por módulo
4. Evitar cerrar bugs distintos como un solo caso
5. Reusar el patrón en la nueva solicitud
```

## Por qué es útil como ejemplo

Representa una solicitud mezclada en la que era necesario separar frentes:

- **listado**: problema de paginación/filtrado en la capa de consulta;
- **totales**: discrepancia de agregación entre dos vistas;
- **notificación**: fallo en la generación o adjunto del correo.

El "todo empezó ayer" sugiere una causa común, pero es una hipótesis, no un hecho. Puede ser un despliegue compartido, o pura coincidencia.

## Trampa que evita

Cerrar los tres síntomas como un solo bug porque comparten fecha. Si la causa raíz resulta ser distinta por frente, el cierre único esconde dos bugs vivos.

## Clasificación esperada

```yaml
primary_capability: qa_bug_diagnosis
secondary_capabilities: [business_intake, architecture_analysis]
confidence: 0.8
needs_human_review: true
```

## Capacidades

- `business_intake`;
- `qa_bug_diagnosis`;
- `architecture_analysis`.

## Preguntas abiertas típicas

- ¿Los tres síntomas ocurren en el mismo ambiente?
- ¿Hubo un despliegue común ayer, o son ventanas distintas?
- ¿Existe evidencia (log, captura, request id) por cada frente?
- ¿Algún frente es bloqueante y los otros no?
