# Capacidades

Una capacidad es un tipo reusable de trabajo.

```text
capability = qué problema resuelve + cuándo aplica + cómo se ejecuta + qué produce + cómo se mide
```

## Quién lo usa / ejecuta

El agente o el runner consultan esta lista después del intake estructurado.

## Orden lógico

```text
1. Intake estructurado
2. Clasificación de capacidad
3. Lectura del YAML correspondiente en capabilities/
4. Selección de modelos/herramientas
5. Producción de outputs
6. Revisión y métricas
```

## Para qué sirve

Sirve para que el orquestador no trate todas las solicitudes igual.

Ejemplo: no es lo mismo una nota de soporte con un screenshot que un hotfix de ambiente o un análisis de arquitectura.

La capacidad elegida define la ruta de trabajo, los modelos y el nivel de revisión humana.

## Capacidades MVP

| Capacidad | Cuándo se usa | Salida |
|---|---|---|
| `business_intake` | El input llega crudo: chat, audio, correo, screenshot o nota de reunión. | request, hechos, supuestos, preguntas. |
| `qa_bug_diagnosis` | Hay un síntoma en QA/STG/PRD y se necesita causa raíz con evidencia. | root cause, evidence, next action. |
| `architecture_analysis` | Se debe diseñar una solución o documentar un ADR/plan. | README, ADR, PLAN, VALIDATION. |
| `support_sop` | Se necesita un SOP (Standard Operating Procedure / procedimiento operativo estándar) repetible para soporte. | SOP, checklist, examples. |
| `environment_promotion` | Hay que mover cambios entre ambientes sin arrastrar commits no aprobados. | drift report, branches, PRs. |
| `implementation` | Ya existe solución aprobada y toca cambiar código. | commits, tests, PR. |
| `research_comparison` | Se quiere comparar alternativas antes de decidir. | trade-offs, recommendation. |

## Regla práctica

1. Clasificar la solicitud.
2. Elegir la capacidad principal.
3. Activar capacidades secundarias si hace falta.
4. Seleccionar el router de modelos.
5. Registrar el resultado y la revisión humana, incluyendo `review_rework_pct` (porcentaje del resultado que tuvo que cambiarse después de revisión humana).

## Reglas transversales

- Separar módulo, cliente, dominio y ambiente.
- No asumir que un screenshot basta como verdad técnica.
- Mantener hechos, supuestos y dudas separados.
- No tocar repos/producto sin aprobación explícita.
- Registrar revisión humana como señal de aprendizaje.

Los detalles operativos viven en `capabilities/*.yaml`.
