# Capacidades

Esta carpeta contiene las capacidades operativas del orquestador.

Cada archivo YAML describe un tipo reusable de trabajo: cuándo aplica, qué perfiles de modelo puede usar, qué herramientas necesita, qué produce y qué métricas se registran.

## Quién lo usa / ejecuta

La invocan el agente o `scripts/run_request.py` después de clasificar una solicitud.

## Orden lógico

```text
1. Recibir clasificación
2. Abrir el YAML de la capacidad principal
3. Leer inputs/models/tools/outputs/rules/metrics
4. Construir ruta recomendada
5. Generar salida en runs/<case-id>/
```

## Para qué sirve

Sirve para que el orquestador no trate todas las solicitudes igual.

Una solicitud puede llegar como chat, screenshot, correo o ticket. La capacidad seleccionada define la ruta de trabajo correcta.

## Cuándo se usa

Se consulta esta carpeta cuando una solicitud ya fue clasificada y hace falta decidir cómo ejecutarla.

Ejemplo:

- `business_intake` para normalizar input crudo;
- `qa_bug_diagnosis` para encontrar causa raíz;
- `architecture_analysis` para generar arquitectura/ADR/plan;
- `support_sop` para documentar un SOP (Standard Operating Procedure / procedimiento operativo estándar);
- `environment_promotion` para mover cambios entre ambientes;
- `implementation` para cambios de código ya aprobados;
- `research_comparison` para comparar alternativas.

## Cómo leerla

Cada YAML describe:

- `description`: intención de la capacidad;
- `inputs`: qué necesita;
- `models`: qué perfiles de modelo son candidatos (ver `config/model-routing.yaml`);
- `tools`: qué herramientas requiere;
- `outputs`: qué archivos o artifacts debe producir;
- `rules`: restricciones y hábitos;
- `metrics`: qué medir después, incluyendo `review_rework_pct` (porcentaje del resultado que tuvo que cambiarse después de revisión humana).

Los candidatos en `models` son perfiles (`generalist`, `deep-reasoning`, `coding`, `budget-reasoning`, `human-review`), no marcas. El mapeo a modelos concretos vive en un solo lugar: `config/model-routing.yaml`.
