# Config

Esta carpeta contiene configuración operativa.

## Quién lo usa / ejecuta

La invocan el agente o los scripts cuando necesitan defaults de routing sin reescribirlos en cada caso.

## Orden lógico

```text
1. Capacidad clasificada
2. Leer config/model-routing.yaml
3. Seleccionar rol y perfil primary/secondary/fallback
4. Registrar métricas esperadas
```

## Para qué sirve

Sirve para guardar valores operativos que el orquestador puede leer sin volver a decidirlos cada vez.

## Archivo principal

### `model-routing.yaml`

Define dos capas:

1. catálogo de modelos (`models`): perfil de capacidad, provider, `model_id`, credencial esperada y estado de readiness;
2. routing por rol (`roles`): primary/secondary/fallback usando IDs de perfil estables, no nombres de marca.

Para adaptarlo a tu entorno, cambia solo el bloque `models`. El bloque `roles` no debería requerir cambios cuando cambia el catálogo.

Roles cubiertos:

- orquestación;
- arquitectura;
- implementación;
- investigación;
- QA/diagnóstico;
- SOP (Standard Operating Procedure / procedimiento operativo estándar) soporte.

Estados de readiness usados:

- `ready`: usable;
- `blocked`: configurado pero no usable por proveedor/billing/límite;
- `missing_key`: no usable porque falta credencial;
- `unknown`: requiere verificación antes de uso.

También lista métricas mínimas a observar:

- `cost_usd`;
- `latency_sec`;
- `human_score`;
- `review_rework_pct` (porcentaje del resultado que tuvo que cambiarse después de revisión humana);
- `accepted`.

## Seguridad

Este archivo no debe contener llaves ni secretos. Solo declara el **nombre** de la variable de entorno esperada en `credential`.
