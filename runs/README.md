# Corridas / runs

Esta carpeta contiene salidas generadas por cada intento o caso trabajado.

## Quién lo usa / ejecuta

La escribe `scripts/run_request.py` durante un dry-run o una ejecución aprobada.

## Orden lógico

```text
1. Recibir inputs/inbox/<case-id>/ o solicitud cruda
2. Ejecutar dry-run
3. Crear runs/<case-id>/
4. Guardar intake, clasificación, hechos, ruta recomendada y review template
5. Humano revisa antes de ejecutar cambios reales
```

## Para qué sirve

Sirve para guardar la evidencia de una corrida del orquestador: qué entró, cómo se clasificó, qué ruta se recomendó y qué dijo la revisión humana.

## Qué significa dry-run

`dry-run` significa simulación sin efectos destructivos.

En un dry-run, el agente o el script puede:

- ordenar la solicitud;
- clasificar la capacidad;
- detectar información faltante;
- recomendar modelos/playbooks;
- preparar archivos de revisión.

Pero no debe:

- crear PRs reales;
- modificar repos de producto;
- tocar producción;
- ejecutar cambios no aprobados.

## Estructura por caso

Cada caso vive en una carpeta propia, por ejemplo:

```text
runs/20260710-case-001/
  01-intake.md
  02-classification.json
  03-facts-and-unknowns.md
  04-recommended-route.md
  05-human-review-template.yaml
```

## Datos sensibles

Los runs pueden contener material real de una solicitud. No comitees runs con información de clientes o empleadores a un repo público. Esta carpeta se distribuye vacía a propósito.

## Sobre `.gitkeep`

El archivo `.gitkeep` solo mantiene la carpeta en Git mientras no hay runs.
