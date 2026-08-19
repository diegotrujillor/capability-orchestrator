# Scripts

Esta carpeta contiene los entrypoints ejecutables del MVP.

## Quién lo usa / ejecuta

Los ejecuta el agente o una persona desde terminal, siempre con aprobación antes de efectos reales.

## Orden lógico

```text
1. run_request.py crea/completa input si hace falta
2. valida schema
3. clasifica capacidad
4. recomienda ruta
5. escribe runs/<case-id>/
```

## Para qué sirve

Sirve para convertir la arquitectura en acciones concretas de forma genérica:

- leer una solicitud cruda o un input parcial;
- construir `inputs/inbox/<case-id>/request.md` lo máximo posible;
- extraer texto básico de Markdown/texto/PPTX;
- generar el intake estructurado;
- clasificar la capacidad con señales generales, no con reglas de un caso específico;
- recomendar tipo de ruta sin inventar nombre de repo ni decisión final;
- preparar la revisión humana.

## Uso

```bash
python scripts/run_request.py --input-dir inputs/inbox/<case-id> --case-id <case-id> --mode dry-run
python scripts/run_request.py --raw "<texto inicial>" --case-id case-001 --mode dry-run
python scripts/run_request.py --input inputs/inbox/<case-id>/request.md --case-id <case-id> --mode dry-run
```

## Previsto, aún no implementado

```bash
python scripts/log_review.py runs/<case-id>/human-review.yaml
python scripts/export_case_note.py runs/<case-id>
```

## Qué significa dry-run

`dry-run` es una simulación: produce archivos de análisis y recomendación, pero no crea PRs ni modifica repos de producto.

## Verificación

```bash
python3 -m unittest discover -s tests -v
```

## Relación con el resto del repo

- `README.md`: explica el flujo general y el primer intento recomendado.
- `MVP.md`: define el objetivo del runner local.
- `runs/`: recibe las salidas de cada corrida.
- `schemas/`: valida la estructura de entrada y revisión.
