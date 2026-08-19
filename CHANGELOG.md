# Registro de cambios

Registro incremental de cambios de esta iniciativa. Mantiene trazabilidad de decisiones, ajustes de enfoque y evolución del diseño.

El objetivo del changelog no es reemplazar Git, sino explicar por qué cambió el artifact y qué decisión o aprendizaje motivó cada incremento.

## 2026-08-19

### Agregado

- Publicación inicial de `capability-orchestrator` como arquitectura reusable y agnóstica para orquestar solicitudes entrantes.
- Definición de la visión central: un orquestador de capacidades, no un único modelo que responde a todo.
- Taxonomía de capacidades en `capabilities/*.yaml`: `business_intake`, `qa_bug_diagnosis`, `architecture_analysis`, `support_sop`, `environment_promotion`.
- Contratos de entrada y revisión humana en `schemas/`.
- Routing de modelos por rol en `MODEL-ROUTING.md` y `config/model-routing.yaml`.
- Runner MVP determinístico `scripts/run_request.py` para dry-runs repetibles desde `--input-dir`, `--input` o `--raw`.
- Prueba automatizada en `tests/test_run_request.py`.
- Documento de modo de trabajo en `docs/WORKING-MODE.md`.
- Casos semilla sintéticos en `examples/`.
- Métricas de calidad y costo en `METRICS.md`, con `review_rework_pct` como métrica central.

### Decisiones de diseño

- **Perfiles de modelo, no marcas.** El routing se expresa en perfiles de capacidad (`generalist`, `deep-reasoning`, `coding`, `budget-reasoning`, `human-review`) y el mapeo a modelos concretos vive en un solo archivo. Así el repo sobrevive al cambio de catálogo de modelos, que ocurre cada pocos meses.
- **Backend de métricas intercambiable.** El repo define qué medir, no dónde guardarlo. Un archivo local, una hoja de cálculo o una plataforma de experiment tracking sirven igual.
- **Proveedor de repositorio agnóstico.** El flujo habla de issues y PRs, no de un proveedor específico.
- **`inputs/` y `runs/` se distribuyen vacíos.** Son las carpetas donde entra material real de una solicitud; mantenerlas vacías en el repo compartido evita filtrar información de terceros.
- **Los ejemplos son sintéticos a propósito.** El valor de un caso semilla está en el patrón, no en el contenido, y un patrón sintético se puede publicar.
- **`review_rework_pct` como métrica central.** Un modelo barato no es barato si obliga a rehacer el trabajo. La métrica que importa no es el costo del token sino el costo total hasta un resultado aceptado.
