# Schemas / contratos

Esta carpeta define los contratos mínimos de entrada y revisión humana.

Los schemas ayudan a que el primer caso llegue con estructura suficiente para trabajar sin perder contexto.

## Quién lo usa / ejecuta

Los invoca el runner antes de procesar una solicitud y al registrar la revisión humana.

## Orden lógico

```text
1. Crear/completar request
2. Validar contra request.schema.json
3. Ejecutar clasificación/routing
4. Humano revisa
5. Validar revisión contra human-review.schema.json
```

## Para qué sirve

Sirve para validar dos momentos:

1. la solicitud que entra;
2. la revisión humana que cierra o corrige el resultado.

## Archivos

### `request.schema.json`

Describe la forma esperada de una solicitud.

Campos principales:

- `title`: título corto del caso;
- `source`: origen del request;
- `raw_request`: texto original;
- `business_context`: cliente, dominio, módulo, ambiente;
- `attachments`: soportes;
- `desired_outcome`: resultado esperado;
- `constraints`: restricciones;
- `known_people`: personas o equipos involucrados.

`business_context` es deliberadamente genérico. Adáptalo a tu dominio sin romper los cuatro ejes: quién, de qué se trata, dónde vive y en qué ambiente.

### `human-review.schema.json`

Describe la respuesta de la revisión humana.

Campos principales:

- `accepted`: si el resultado se aprueba o no;
- `human_score`: nota humana;
- `review_rework_pct`: porcentaje del resultado que tuvo que cambiarse después de revisión humana;
- `comments`: observaciones;
- `reusable_lessons`: aprendizajes que sí deben quedar;
- `follow_up_actions`: siguientes pasos;
- `metrics_run_url`: enlace al run registrado;
- `architecture_repo_url`: enlace al repo o artifact final.
