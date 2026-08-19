# MVP

Objetivo: validar el orquestador sin construir plataforma pesada.

## Quién lo usa / ejecuta

Inicialmente lo ejecuta un agente con aprobación humana. También puede ejecutarse como script local.

## Orden lógico

```text
1. Recibir solicitud cruda
2. Crear/completar el request automáticamente hasta donde sea posible
3. Marcar dudas como preguntas abiertas
4. Ejecutar dry-run (simulación sin tocar repos ni crear PRs)
5. Generar runs/<case-id>/
6. Revisar humanamente
7. Ejecutar solo lo aprobado
```

## Qué problema resuelve

Hoy una solicitud llega mezclada y se pierde tiempo en:

- reexplicar contexto;
- adivinar el tipo de trabajo;
- decidir qué modelo usar;
- recordar qué artifact producir;
- revisar manualmente qué se cambió.

El MVP existe para estandarizar ese primer paso.

## Qué hace el MVP

El MVP toma una solicitud cruda y genera una salida estructurada para revisión humana.

Debe responder:

1. ¿Qué tipo de solicitud es?
2. ¿Qué información falta?
3. ¿Qué capacidad se activa?
4. ¿Qué ruta de modelos/playbook conviene?
5. ¿Qué artifacts se deben producir?

## Fase 0

- Taxonomía de capacidades.
- Router de modelos.
- Schemas de request y human review.
- Métricas.
- Casos semilla.

## Fase 1

Runner local, con generación de input cuando sea posible:

```bash
python scripts/run_request.py --raw "<texto inicial del caso>" --case-id case-001 --mode dry-run
```

Si ya existe un archivo parcial:

```bash
python scripts/run_request.py --input inputs/inbox/<case-id>/request.md --mode dry-run
```

`dry-run` significa simulación: el runner ordena, clasifica y recomienda, pero no crea PRs, no modifica repos de producto y no ejecuta cambios destructivos.

Salida:

```text
runs/<case-id>/
  01-intake.md
  02-classification.json
  03-facts-and-unknowns.md
  04-recommended-route.md
  05-human-review-template.yaml
```

### Intención de la salida

- `01-intake.md`: dejar la solicitud limpia y resumida.
- `02-classification.json`: mostrar qué capacidad se activó y con qué confianza.
- `03-facts-and-unknowns.md`: separar lo confirmado de lo pendiente.
- `04-recommended-route.md`: explicar qué modelo/playbook usar y por qué.
- `05-human-review-template.yaml`: preparar la revisión humana y la captura de `review_rework_pct` (porcentaje del resultado que tuvo que cambiarse después de revisión humana).

## No hacer aún

- PRs automáticos sin aprobación.
- Cambios en producción.
- UI web.

## Éxito

El MVP sirve si reduce repetición de contexto y deja claro el camino de trabajo antes de ejecutar.
