# Ejemplos

Casos semilla sintéticos para probar el orquestador con patrones recurrentes.

Los ejemplos son ilustrativos y no contienen datos de ningún cliente ni sistema real.

## Quién lo usa / ejecuta

Los consulta el agente o la persona cuando una nueva solicitud se parece a un caso previo.

## Orden lógico

```text
1. Leer solicitud nueva
2. Buscar ejemplo parecido
3. Reusar patrón, no copiar ciegamente la solución
4. Registrar diferencias del nuevo caso
```

## Caso 1: reporte de QA con frentes mezclados

Situación: una sola solicitud describe varios síntomas que en realidad pertenecen a módulos distintos.

Patrón reusable:

- una solicitud puede mezclar frentes funcionales;
- separar cada frente antes de diagnosticar;
- no cerrar síntomas distintos como un solo bug;
- preservar evidencia original.

Capacidades:

- `business_intake`;
- `qa_bug_diagnosis`;
- `architecture_analysis`.

Ver [`examples/mixed-qa-report/`](./examples/mixed-qa-report/).

## Caso 2: feature con ciclo completo hasta producción

Situación: una solicitud requiere diseño, implementación, guía de soporte y promoción entre ambientes.

Patrón reusable:

- arquitectura antes de código;
- implementación de datos antes que la de API cuando hay dependencia;
- SOP (Standard Operating Procedure / procedimiento operativo estándar) de soporte como entregable de primera clase;
- verificación en la rama de producción;
- reconciliación del hotfix hacia ramas activas.

Capacidades:

- `architecture_analysis`;
- `support_sop`;
- `environment_promotion`.

Ver [`examples/full-cycle-feature/`](./examples/full-cycle-feature/).
