# Entradas

Esta carpeta contiene material de entrada para una nueva solicitud antes de que el orquestador genere un run.

## Para qué sirve

Sirve como bandeja simple para los archivos iniciales que llegan con un requerimiento: texto, notas, screenshots referenciados, tickets exportados, correos copiados, logs o cualquier soporte que ayude a construir el intake.

## Quién lo usa / ejecuta

La leen el agente o `scripts/run_request.py` al iniciar un caso.

## Orden lógico

```text
1. Crear una carpeta por caso en inputs/inbox/<case-id>/
2. Poner allí todos los archivos recibidos
3. El agente/runner construye inputs/inbox/<case-id>/request.md lo máximo posible
4. Ejecutar dry-run
5. El resultado se escribe en runs/<case-id>/
6. Después de revisión, mover o marcar el input como procesado
```

## Estructura recomendada

Para un requerimiento con varios archivos, usa una carpeta propia:

```text
inputs/inbox/20260710-nuevo-requerimiento/
  raw-request.md
  screenshot-01.png
  correo-soporte.md
  log-error.txt
  links.md
```

## Qué debe hacer el agente o el runner

No debe exigir que la persona complete todo manualmente.

Debe leer lo disponible y construir el mejor intake posible:

```text
inputs/inbox/<case-id>/request.md
```

Si algo falta, debe dejarlo como pregunta abierta. No debe inventar cliente, módulo, ambiente, responsable ni causa raíz.

## Qué no va aquí

- artifacts finales;
- PRs;
- decisiones cerradas;
- histórico permanente de todos los requerimientos.

Esta carpeta es entrada de trabajo, no archivo histórico definitivo.

## Datos sensibles

El material de entrada suele ser el más sensible del flujo. No comitees inputs reales de clientes o empleadores a un repo público. Esta carpeta se distribuye vacía a propósito.
