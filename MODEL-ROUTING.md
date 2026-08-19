# Routing de modelos

Hipótesis inicial para enrutar trabajo por rol/capacidad. No es una verdad fija: las métricas deben validar qué combinación reduce costo, tiempo y rework humano.

## Quién lo usa / ejecuta

Lo consulta el agente o el runner cuando ya existe una clasificación de capacidad.

## Orden lógico

```text
1. Clasificar capacidad
2. Elegir rol principal
3. Seleccionar primary
4. Verificar readiness del modelo seleccionado
5. Usar secondary para contraste, crítica o si primary no está listo
6. Usar fallback si baja confianza, falla proveedor, sube costo/rework o no hay modelo listo
7. Registrar métricas
```

## Perfiles de modelo, no marcas

El routing se define por **perfil de capacidad**, no por proveedor. Así el repo sobrevive al cambio de catálogo de modelos.

| ID de perfil | Qué se espera de él |
|---|---|
| `deep-reasoning` | Razonamiento largo y trade-offs; diseño y arquitectura. |
| `generalist` | Fuerte de propósito general; orquestación, investigación, síntesis. |
| `coding` | Especializado en generar y modificar código con tests. |
| `budget-reasoning` | Razonamiento aceptable a bajo costo; exploración y fallback. |
| `human-review` | Persona revisora; fallback no-modelo, siempre disponible. |

El mapeo perfil -> modelo concreto vive en `config/model-routing.yaml`, en un solo lugar.

## Mapa visual

```text
Orquestador
  |
  +-- Arquitectura
  |     primary:   deep-reasoning
  |     secondary: generalist
  |     fallback:  budget-reasoning
  |
  +-- Implementación
  |     primary:   coding
  |     secondary: generalist
  |     fallback:  human-review
  |
  +-- Investigación
        primary:   generalist
        secondary: budget-reasoning
        fallback:  deep-reasoning (síntesis final)
```

## Catálogo operativo

`config/model-routing.yaml` mantiene dos capas separadas:

1. catálogo operativo de modelos (`models`): perfil, provider, `model_id`, credencial esperada y readiness;
2. routing por rol (`roles`): primary/secondary/fallback usando IDs de perfil estables, no nombres libres.

La política operativa es: no usar modelos bloqueados o sin llave de forma silenciosa. Si el primary no está disponible, intentar secondary; si tampoco está disponible, intentar fallback; si no hay modelo listo, pedir revisión humana.

## Roles

| Rol | Primary | Secondary | Fallback | Cuándo usar |
|---|---|---|---|---|
| Orquestación | `generalist` | - | `human-review` | Clasifica, decide ruta, pide aprobación. |
| Arquitectura | `deep-reasoning` | `generalist` | `budget-reasoning` | Solución, ADR, planes, trade-offs. |
| Implementación | `coding` | `generalist` | `human-review` | Código, tests, branches, PRs. |
| Investigación | `generalist` | `budget-reasoning` | `deep-reasoning` | Comparar alternativas, validar hipótesis, sintetizar. |
| QA / diagnóstico | `generalist` | `budget-reasoning` | `coding` si hay fix | Separar causa raíz de síntomas. |
| SOP soporte | `generalist` | `deep-reasoning` | `human-review` | Guías claras y ejecutables. |

## Estados de readiness

- `ready`: usable;
- `blocked`: configurado pero no usable por proveedor/billing/límite;
- `missing_key`: no usable porque falta credencial;
- `unknown`: requiere verificación antes de uso.

## Regla de decisión

1. Clasificar capacidad.
2. Seleccionar primary.
3. Verificar que el modelo tenga readiness `ready`.
4. Usar secondary si el primary está bloqueado/no configurado, falta claridad, crítica o contraste.
5. Usar fallback si hay costo alto, falla de proveedor/modelo o baja confianza.
6. Si ningún modelo está listo, pedir revisión humana.
7. Registrar métricas:
   - modelo usado;
   - rol;
   - costo;
   - latencia;
   - score humano;
   - `review_rework_pct` (porcentaje del resultado que tuvo que cambiarse después de revisión humana).

## Nota

El routing debe evolucionar con evidencia. Si un modelo barato genera mucho rework, no es realmente barato.

Este archivo documenta la intención y la disponibilidad verificada; no activa todavía un motor runtime de selección automática.
