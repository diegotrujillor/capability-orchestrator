# Primer uso

Guía mínima para usar el orquestador con un requerimiento real.

## Idea principal

No necesitas escribir un intake perfecto manualmente.

Si tienes 3 o 4 archivos de entrada, ponlos en una carpeta por caso y deja que el agente o el runner construyan el `request.md` lo máximo posible.

## Paso 1: crear carpeta del caso

```text
inputs/inbox/20260710-nuevo-requerimiento/
```

Ejemplo con varios archivos:

```text
inputs/inbox/20260710-nuevo-requerimiento/
  raw-request.md
  screenshot-01.png
  correo-soporte.md
  log-error.txt
  links.md
```

## Paso 2: correr dry-run

```bash
python scripts/run_request.py \
  --input-dir inputs/inbox/20260710-nuevo-requerimiento \
  --case-id 20260710-nuevo-requerimiento \
  --mode dry-run
```

`dry-run` significa simulación: ordena, clasifica y recomienda, pero no crea PRs, no modifica repos de producto y no toca producción.

## Paso 3: revisar salida

El resultado esperado vive en:

```text
runs/20260710-nuevo-requerimiento/
  01-intake.md
  02-classification.json
  03-facts-and-unknowns.md
  04-recommended-route.md
  05-human-review-template.yaml
```

## Paso 4: recibir recomendación y aprobar destino real

Después de la revisión, el orquestador recomienda el destino real. La persona aprueba o corrige esa recomendación.

El caso puede ir a:

- issue o PR;
- repo de arquitectura específico;
- artifact/SOP (Standard Operating Procedure / procedimiento operativo estándar) aprobado;
- cierre con preguntas abiertas si falta información.

## Regla importante

Todas las solicitudes pueden pasar por la lógica del orquestador.
No todas las solicitudes deben vivir permanentemente en este repo.

## Después de los primeros 3 a 5 casos

Al principio este repo puede guardar algunos casos piloto para aprender el proceso.

Después de esos primeros casos, si recibes archivos dispersos pero no existe repo, issue ni PR todavía, procede así:

```text
1. Crear un contenedor temporal del caso fuera del histórico permanente.
2. Pasar esos archivos por la lógica del orquestador.
3. Generar intake + clasificación + ruta recomendada.
4. Decidir el destino real.
5. Mover el caso al destino real y dejar en este repo solo ejemplo o referencia mínima si aporta aprendizaje.
```

Destinos recomendados:

| Caso | Dónde debería vivir |
|---|---|
| Bug o soporte operativo | Issue o ticket operativo. |
| Cambio de código | Issue/PR en el repo producto. |
| Nueva solución o decisión técnica | Repo de arquitectura específico. |
| Procedimiento repetible | Artifact/SOP aprobado. |
| Falta información | Preguntas abiertas en el canal/issue correspondiente. |

Regla práctica:

```text
Usa este repo para procesar y aprender el patrón.
No lo uses como archivo histórico de todos los adjuntos reales.
```

## Advertencia sobre datos sensibles

`inputs/` y `runs/` pueden contener material real de una solicitud. Si trabajas con información de un cliente o empleador:

- no comitees ese material a un repo público;
- mantén `inputs/inbox/` e `runs/` vacíos en el repo compartido, o ignóralos localmente;
- usa ejemplos sintéticos cuando quieras documentar un patrón.
