# Métricas

El tracking de métricas observa; no orquesta.

Su propósito es medir qué ruta de trabajo produce mejor resultado real con menor costo y menor rework humano.

Cualquier backend sirve: un archivo local, una hoja de cálculo o una plataforma de experiment tracking. Este repo define qué medir, no dónde guardarlo.

## Quién lo usa / ejecuta

Lo invoca el runner al cerrar una corrida o al registrar una revisión humana.

## Orden lógico

```text
1. Runner genera output
2. Humano revisa
3. Se calcula score y review_rework_pct (porcentaje del resultado que tuvo que cambiarse después de revisión humana)
4. Se registra el run
5. Se comparan rutas con evidencia
```

## Qué significa `pct`

`pct` = percentage = porcentaje.

## Métrica clave

```yaml
review_rework_pct: 0-100  # porcentaje del resultado que tuvo que cambiarse después de revisión humana
```

Ejemplo:

- 0% = el humano no cambió nada;
- 20% = hubo ajustes moderados;
- 80% = la salida inicial no estaba lista y se rehizo gran parte.

Un modelo barato no es barato si obliga a rehacer mucho trabajo.

## Qué queremos responder

- ¿Qué capacidad estamos resolviendo?
- ¿Qué modelo tomó el rol principal?
- ¿Qué modelo funcionó como secondary o fallback?
- ¿Cuánto costó?
- ¿Cuánto tardó?
- ¿Cuánto rework hizo el humano?
- ¿Se aceptó o se rechazó el resultado?

## Métricas mínimas

```yaml
case_id: 20260710-001
capability: qa_bug_diagnosis
model_route:
  architecture: deep-reasoning
  implementation: coding
  research: generalist
cost_usd: 0.43
latency_sec: 312
human_score: 8.5
review_rework_pct: 12  # 12% del resultado cambió después de revisión humana
accepted: true
business_outcome: fixed
```

## Para qué sirve

Con suficientes runs, el orquestador debería aprender rutas más efectivas.

Ejemplo de hipótesis a validar:

- un generalista fuerte puede servir para consolidar evidencia;
- un modelo especializado en código puede servir para implementación;
- un modelo económico de razonamiento puede servir como exploración o fallback barato.

## Qué se guarda

- intake estructurado;
- classification JSON;
- output final;
- links a issues/PRs;
- human review;
- métricas del run.

## Decisión esperada

Las métricas no deciden por sí solas. Solo permiten comparar rutas con evidencia y evitar decisiones basadas en intuición o recuerdo parcial.
