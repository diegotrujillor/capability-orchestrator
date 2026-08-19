# Modo de trabajo con Capability Router

## Propósito

Este documento resume cómo usar `capability-router` como fábrica de trabajo para solicitudes entrantes.

La idea no es guardar toda la operación dentro de este repo. La idea es usar este repo para convertir material disperso en una ruta clara, trazable y aprobable.

```text
Todas las solicitudes pueden pasar por la lógica del orquestador.
No todas las solicitudes deben vivir dentro de este repo.
```

## Qué problema resuelve

Antes, cada solicitud podía llegar por chat, reunión, correo, ticket, screenshot o archivo suelto. La persona que la recibía debía reconstruir contexto, recordar restricciones, decidir si era arquitectura, bug, soporte, implementación o investigación, y luego crear manualmente el artifact correcto.

Con este modo de trabajo, cada solicitud pasa primero por un intake y una clasificación mínima.

El resultado esperado es:

- entender qué se pidió;
- separar hechos, supuestos y preguntas abiertas;
- clasificar la capacidad requerida;
- recomendar el destino real;
- pedir aprobación humana antes de tocar repos, PRs o producción;
- dejar aprendizaje reusable para el siguiente caso.

## Qué es este repo

Este repo es la fábrica/orquestador.

Sirve para:

- definir el formato de entrada;
- clasificar solicitudes;
- definir capacidades;
- definir routing de modelos;
- generar dry-runs;
- preparar revisión humana;
- guardar ejemplos sintéticos;
- documentar el modo de trabajo.

No sirve para:

- almacenar permanentemente todos los requerimientos;
- reemplazar issues/PRs;
- acumular todos los adjuntos históricos;
- ejecutar cambios de producto sin aprobación;
- decidir arquitectura sin inspección real.

## Lifecycle recomendado

```text
Fase 0: Intake, clasificación y decisión de destino
        ↓
Fase 1: Descubrimiento técnico
        ↓
Fase 2: Análisis arquitectura actual vs propuesta
        ↓
Fase 3: ADR / decisión técnica
        ↓
Fase 4: PoC o plan incremental
        ↓
Fase 5: Implementación aprobada
```

## Fase 0: Intake, clasificación y decisión de destino

Esta fase ocurre en `capability-router`.

Objetivo: convertir archivos dispersos en una solicitud entendible y una ruta recomendada.

### Entrada

Material recibido, por ejemplo:

- transcripción de reunión;
- screenshot;
- presentación;
- correo;
- ticket;
- notas de chat;
- logs;
- links.

### Dónde poner los archivos

```text
inputs/inbox/<case-id>/
```

Ejemplo:

```text
inputs/inbox/20260710-nuevo-requerimiento/
  input-1.md
  input-2.md
  input-3.png
  input-4.pptx
```

### Comando

```bash
python3 scripts/run_request.py \
  --input-dir inputs/inbox/<case-id> \
  --case-id <case-id> \
  --mode dry-run
```

`dry-run` significa simulación sin efectos destructivos. Puede generar análisis, clasificación y recomendaciones, pero no crea PRs, no modifica repos de producto y no toca producción.

### Salida

```text
runs/<case-id>/
  01-intake.md
  02-classification.json
  03-facts-and-unknowns.md
  04-recommended-route.md
  05-human-review-template.yaml
```

### Decisión humana

El orquestador recomienda el destino real. La persona revisora aprueba o corrige.

Posibles destinos:

- issue;
- PR en repo de producto;
- repo específico de arquitectura;
- artifact/SOP (Standard Operating Procedure / procedimiento operativo estándar);
- preguntas abiertas si falta información;
- descarte si no aplica.

## Fase 1: Descubrimiento técnico

Esta fase ocurre en el destino real aprobado, no necesariamente en el orquestador.

Si el destino es un repo de arquitectura, ahí se empieza a trabajar.

Objetivo:

- confirmar repos involucrados;
- inspeccionar código, SQL, diagramas de proceso o configuración real;
- validar si la hipótesis inicial coincide con la realidad;
- separar información confirmada de supuestos;
- actualizar preguntas abiertas.

Regla importante:

```text
No confiar solo en transcripciones o screenshots.
Verificar contra fuente real cuando exista.
```

## Fase 2: Análisis arquitectura actual vs propuesta

Objetivo: contrastar el estado actual con la propuesta.

Preguntas típicas:

- ¿Cómo funciona hoy?
- ¿Dónde está el acoplamiento?
- ¿Qué parte de la propuesta reduce deuda real?
- ¿Qué riesgos introduce?
- ¿Qué componentes deberían existir?
- ¿Qué queda fuera del MVP?

Output esperado:

- diagrama o explicación del flujo actual;
- diagrama o explicación del flujo propuesto;
- riesgos;
- dependencias;
- preguntas pendientes.

## Fase 3: ADR / decisión técnica

ADR significa Architecture Decision Record / registro de decisión arquitectónica.

Objetivo: dejar una decisión revisable, no solo una conversación.

Debe incluir:

- contexto;
- decisión propuesta;
- alternativas consideradas;
- consecuencias positivas;
- riesgos;
- validación pendiente;
- criterio para avanzar o descartar.

## Fase 4: PoC o plan incremental

PoC significa Proof of Concept / prueba de concepto.

Objetivo: validar una parte pequeña antes de comprometer implementación amplia.

Opciones:

- PoC aislada sin tocar producto;
- plan incremental sobre un caso piloto;
- refactor mínimo en repo producto;
- postergación si el riesgo supera el beneficio.

Regla:

```text
No convertir una visión completa en implementación grande sin pasar por una validación pequeña.
```

## Fase 5: Implementación aprobada

Solo ocurre si hay aprobación explícita.

Puede incluir:

- branch de implementación;
- PR;
- pruebas;
- actualización de CHANGELOG del repo producto;
- documentación de despliegue;
- plan de rollback o mitigación.

No debe ocurrir si todavía hay preguntas críticas abiertas.

## Roles esperados

### El agente / orquestador

- estructura el material;
- genera intake;
- clasifica capacidad;
- recomienda ruta;
- propone destino;
- identifica hechos, supuestos y preguntas;
- prepara artifacts iniciales;
- no ejecuta cambios destructivos sin aprobación.

### Persona revisora

- aprueba o corrige la clasificación;
- aprueba o corrige el destino real;
- define si se involucran otras personas;
- confirma alcance;
- decide si se pasa a descubrimiento, ADR, PoC o implementación.

### Equipo

- aporta contexto real;
- confirma repos/sistemas;
- revisa riesgos;
- valida si el output es útil;
- evita que el orquestador se vuelva un basurero operativo.

## Regla de seguridad

Antes de cualquier acción con efecto real:

```text
El orquestador recomienda.
La persona aprueba.
Luego se ejecuta.
```

Esto aplica para:

- crear repos;
- crear PRs;
- tocar producto;
- tocar producción;
- ejecutar scripts destructivos;
- involucrar a otros equipos.

## Mensaje sugerido para usar con el agente

```text
Usa capability-router para este nuevo requerimiento.
Crea el intake inicial, clasifica la capacidad, lista hechos/supuestos/preguntas y recomienda dónde debería vivir el trabajo.
No crees repos, issues, branches ni PRs hasta que yo apruebe el destino.

Material recibido:
<pegar texto o indicar carpeta de archivos>
```

## Resumen ejecutivo

El orquestador no reemplaza al equipo. Ordena la entrada, recomienda la ruta y hace trazable la decisión.

El valor está en que cada requerimiento empiece con claridad:

```text
qué es,
qué falta,
qué capacidad requiere,
dónde debe vivir,
qué se puede hacer sin riesgo,
y qué necesita aprobación humana.
```
