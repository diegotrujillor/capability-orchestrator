#!/usr/bin/env python3
"""Dry-run runner for the Capability Orchestrator MVP.

This runner is intentionally deterministic and local-only. It reads raw files,
builds/uses request.md, writes runs/<case-id>/ outputs, and never creates PRs,
repos, or product changes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from zipfile import BadZipFile, ZipFile


@dataclass
class InputMaterial:
    files: list[Path]
    text: str
    slide_text: str


def slug_from_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9áéíóúñü]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "case"


def read_pptx_text(path: Path) -> str:
    try:
        with ZipFile(path) as zf:
            slide_names = [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]

            def slide_number(name: str) -> int:
                match = re.search(r"slide(\d+)", name)
                return int(match.group(1)) if match else 0

            slides = sorted(slide_names, key=slide_number)
            chunks: list[str] = []
            for idx, name in enumerate(slides, 1):
                xml = zf.read(name).decode("utf-8", errors="ignore")
                texts = [unescape(t) for t in re.findall(r"<a:t>(.*?)</a:t>", xml)]
                if texts:
                    chunks.append(f"Slide {idx}: " + " | ".join(texts))
            return "\n".join(chunks)
    except (BadZipFile, FileNotFoundError, KeyError):
        return ""


def collect_input_material(input_dir: Path | None, input_file: Path | None, raw: str | None) -> InputMaterial:
    files: list[Path] = []
    chunks: list[str] = []
    slide_chunks: list[str] = []

    if raw:
        chunks.append(raw)

    if input_file:
        files.append(input_file)
        if input_file.suffix.lower() in {".md", ".txt"}:
            chunks.append(input_file.read_text(encoding="utf-8", errors="ignore"))

    if input_dir:
        for path in sorted(p for p in input_dir.iterdir() if p.is_file() and p.name != "request.md"):
            files.append(path)
            suffix = path.suffix.lower()
            if suffix in {".md", ".txt", ".csv", ".log"}:
                txt = path.read_text(encoding="utf-8", errors="ignore")
                if "data:image/png;base64" not in txt[:500]:
                    chunks.append(f"\n\n# {path.name}\n{txt}")
            elif suffix == ".pptx":
                ppt_text = read_pptx_text(path)
                if ppt_text:
                    slide_chunks.append(ppt_text)

    return InputMaterial(files=files, text="\n".join(chunks).strip(), slide_text="\n".join(slide_chunks).strip())


def infer_title(material: InputMaterial, case_id: str) -> str:
    for source in (material.text, material.slide_text):
        for raw_line in source.splitlines():
            line = raw_line.strip().strip("#`).: ")
            if 12 <= len(line) <= 120 and not line.startswith("!"):
                return line
    return case_id.replace("-", " ").capitalize()


def infer_primary_capability(material: InputMaterial) -> str:
    combined = f"{material.text}\n{material.slide_text}".lower()
    architecture_terms = ["arquitectura", "diseño", "rediseño", "propuesta", "refactor", "acoplamiento", "componentes", "deuda técnica", "escalabilidad"]
    bug_terms = ["error", "qa", "bug", "falla", "no descarga", "traceback"]
    sop_terms = ["procedimiento", "paso a paso", "soporte", "operación"]
    if sum(term in combined for term in architecture_terms) >= 2:
        return "architecture_analysis"
    if any(term in combined for term in bug_terms):
        return "qa_bug_diagnosis"
    if any(term in combined for term in sop_terms):
        return "support_sop"
    return "business_intake"


def secondary_capabilities(primary: str) -> list[str]:
    if primary == "architecture_analysis":
        return ["business_intake", "research_comparison", "implementation"]
    if primary == "qa_bug_diagnosis":
        return ["business_intake", "architecture_analysis"]
    if primary == "support_sop":
        return ["business_intake"]
    return ["architecture_analysis"]


def build_request_md(case_id: str, material: InputMaterial) -> str:
    title = infer_title(material, case_id)
    raw_summary = material.text[:1800].strip() or "Material recibido sin texto extraíble automáticamente. Revisar adjuntos."
    if material.slide_text:
        raw_summary += "\n\nTexto extraído de presentación:\n" + material.slide_text[:1200]

    attachments = "\n".join(f"- `{p.name}`" for p in material.files) or "- ninguno"

    return f"""# Solicitud

## Título

{title}

## Origen

Material recibido en `inputs/inbox/{case_id}/`.

## Solicitud original

{raw_summary}

## Contexto de negocio

- cliente: por confirmar.
- dominio: por confirmar.
- módulo: por confirmar.
- ambiente: por confirmar.

## Resultado esperado

Generar un intake estructurado, clasificar la capacidad y recomendar destino real sin ejecutar cambios destructivos.

## Restricciones

- No tocar repos de producto todavía.
- No crear PRs.
- No asumir información faltante.
- Dejar preguntas abiertas cuando falte contexto.

## Personas involucradas

- por confirmar.

## Adjuntos / referencias

{attachments}

## Preguntas abiertas

- ¿Cuál es el destino real aprobado para este caso?
- ¿Qué repos o sistemas deben inspeccionarse si se aprueba continuar?
- ¿Qué información del material recibido debe tratarse como hecho confirmado?
"""


def ensure_request(case_id: str, input_dir: Path | None, input_file: Path | None, raw: str | None, material: InputMaterial) -> Path | None:
    if input_file:
        return input_file
    if input_dir:
        request_path = input_dir / "request.md"
        if not request_path.exists():
            request_path.write_text(build_request_md(case_id, material), encoding="utf-8")
        return request_path
    return None


def extract_people(text: str) -> list[str]:
    candidates = re.findall(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", text)
    ignored = {"Reunión", "Material", "Texto", "Slide", "Nota", "Correo", "Ticket", "Documento", "Anexo", "Resumen", "Solicitud"}
    names: list[str] = []
    for candidate in candidates:
        if candidate not in ignored and candidate not in names:
            names.append(candidate)
        if len(names) >= 8:
            break
    return names or ["por confirmar"]


def facts_for(primary: str, material: InputMaterial) -> tuple[list[str], list[str], list[str]]:
    combined = f"{material.text}\n{material.slide_text}".lower()
    facts = ["El material fue recibido como insumo para un dry-run del orquestador."]
    assumptions = ["La clasificación es preliminar y requiere revisión humana."]
    questions = [
        "¿Cuál es el destino real aprobado para este caso?",
        "¿Qué repos/sistemas deben inspeccionarse si se aprueba continuar?",
        "¿Qué información del material recibido debe tratarse como hecho confirmado?",
    ]
    if primary == "architecture_analysis":
        facts.append("La solicitud tiene señales de análisis arquitectónico o rediseño técnico.")
        assumptions.append("Podría requerir un repo de arquitectura específico si el análisis continúa.")
        questions.extend([
            "¿Cuál es el límite del MVP: análisis, ADR, PoC o implementación?",
            "¿Quién debe aprobar la arquitectura antes de tocar repos producto?",
        ])

    detected_terms = []
    for term in ["arquitectura", "diseño", "rediseño", "propuesta", "refactor", "acoplamiento", "componentes", "deuda técnica", "escalabilidad", "error", "qa", "bug", "procedimiento", "soporte"]:
        if term in combined and term not in detected_terms:
            detected_terms.append(term)
    if detected_terms:
        facts.append("Términos/señales detectadas: " + ", ".join(detected_terms[:8]) + ".")
        questions.append("¿Qué señales detectadas son realmente relevantes y cuáles son ruido del insumo?")

    return facts, assumptions, questions


def write_outputs(case_id: str, output_root: Path, request_path: Path | None, material: InputMaterial) -> Path:
    out = output_root / case_id
    out.mkdir(parents=True, exist_ok=True)
    title = infer_title(material, case_id)
    primary = infer_primary_capability(material)
    secondary = secondary_capabilities(primary)
    facts, assumptions, questions = facts_for(primary, material)
    people = extract_people(material.text)
    attachments = "\n".join(f"- `{p.name}`" for p in material.files) or "- ninguno"

    intake = f"""# Intake estructurado

## Caso

`{case_id}`

## Resumen

{title}

## Material recibido

{attachments}

## Personas detectadas

""" + "\n".join(f"- {p}" for p in people) + f"""

## Resultado esperado del dry-run

Generar intake estructurado, clasificación, hechos/preguntas, ruta recomendada y formato de revisión humana.

## Request base

{request_path or 'No aplica'}
"""
    (out / "01-intake.md").write_text(intake, encoding="utf-8")

    classification = {
        "case_id": case_id,
        "primary_capability": primary,
        "secondary_capabilities": secondary,
        "confidence": 0.72 if primary == "business_intake" else 0.84,
        "needs_human_review": True,
        "reasoning": {
            primary: "Clasificación inferida por palabras clave y material recibido; requiere revisión humana.",
            "business_intake": "El material requiere normalización, hechos, supuestos y preguntas abiertas.",
        },
        "recommended_destination": {
            "type": "architecture_repo_candidate" if primary == "architecture_analysis" else "open_questions_or_issue_candidate",
            "suggested_name": None,
            "requires_human_approval": True,
        },
    }
    (out / "02-classification.json").write_text(json.dumps(classification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    facts_md = "# Hechos, supuestos y preguntas abiertas\n\n## Hechos confirmados por los insumos\n\n"
    facts_md += "\n".join(f"- {f}" for f in facts)
    facts_md += "\n\n## Supuestos razonables, no confirmados\n\n"
    facts_md += "\n".join(f"- {a}" for a in assumptions)
    facts_md += "\n\n## Preguntas abiertas\n\n"
    facts_md += "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1)) + "\n"
    (out / "03-facts-and-unknowns.md").write_text(facts_md, encoding="utf-8")

    route = f"""# Ruta recomendada

## Decisión sugerida

El orquestador recomienda tratar este caso como `{primary}` y no ejecutar cambios destructivos durante el dry-run.

## Destino recomendado

"""
    if primary == "architecture_analysis":
        route += "Crear un repo de arquitectura específico solo si la persona revisora aprueba el destino y el nombre.\n"
    else:
        route += "Mantener como preguntas abiertas o issue operativo hasta que una persona apruebe el destino real.\n"
    route += f"""
## Ruta de capacidades

```yaml
primary_capability: {primary}
secondary_capabilities:
"""
    route += "\n".join(f"  - {s}" for s in secondary)
    route += "\nneeds_human_review: true\n```\n\n"
    route += """## No hacer todavía

- No tocar repos producto.
- No crear PR.
- No crear repo específico sin aprobación explícita.
- No asumir información faltante.

## Aprobación requerida

La persona revisora debe aprobar o corregir la ruta recomendada antes del siguiente paso.
"""
    (out / "04-recommended-route.md").write_text(route, encoding="utf-8")

    review = f"""case_id: {case_id}
accepted: null
human_score: null
review_rework_pct: null  # porcentaje del resultado que tuvo que cambiarse después de revisión humana
recommended_destination_approved: null
approved_destination:
  type: null # issue | pr | architecture_repo | sop_artifact | open_questions | discard
  url: null
comments: []
corrections_needed:
  - Revisar clasificación y destino recomendado.
reusable_lessons: []
follow_up_actions:
  - Revisar 01-intake.md.
  - Revisar 03-facts-and-unknowns.md.
  - Aprobar o corregir 04-recommended-route.md.
metrics_run_url: null
architecture_repo_url: null
"""
    (out / "05-human-review-template.yaml").write_text(review, encoding="utf-8")
    return out


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local dry-run for an incoming request.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-dir", type=Path)
    source.add_argument("--input", dest="input_file", type=Path)
    source.add_argument("--raw", type=str)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--mode", choices=["dry-run"], default="dry-run")
    parser.add_argument("--output-root", type=Path, default=Path("runs"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_dir = args.input_dir
    input_file = args.input_file
    if input_dir and not input_dir.exists():
        print(f"input-dir does not exist: {input_dir}", file=sys.stderr)
        return 2
    if input_file and not input_file.exists():
        print(f"input file does not exist: {input_file}", file=sys.stderr)
        return 2

    material = collect_input_material(input_dir, input_file, args.raw)
    request_path = ensure_request(args.case_id, input_dir, input_file, args.raw, material)
    run_dir = write_outputs(args.case_id, args.output_root, request_path, material)
    print(f"dry-run ok: {run_dir}")
    print("next: review 04-recommended-route.md and approve/correct destination")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
