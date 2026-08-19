import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RunRequestTest(unittest.TestCase):
    def test_input_dir_creates_request_and_dry_run_outputs(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            case_id = "case-test"
            input_dir = tmp_path / "inputs" / "inbox" / case_id
            input_dir.mkdir(parents=True)
            (input_dir / "input-1.md").write_text(
                """
                Nota sobre la propuesta de rediseño del servicio de notificaciones.
                El diseño actual tiene mucho acoplamiento entre sus componentes.
                Se propone un refactor por capas para mejorar la escalabilidad.
                Hay deuda técnica acumulada. No tocar producto todavía.
                """,
                encoding="utf-8",
            )
            (input_dir / "input-2.pptx").write_bytes(b"not-a-real-pptx")
            output_root = tmp_path / "runs"

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo / "scripts" / "run_request.py"),
                    "--input-dir",
                    str(input_dir),
                    "--case-id",
                    case_id,
                    "--mode",
                    "dry-run",
                    "--output-root",
                    str(output_root),
                ],
                cwd=repo,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((input_dir / "request.md").exists())
            run_dir = output_root / case_id
            expected = [
                "01-intake.md",
                "02-classification.json",
                "03-facts-and-unknowns.md",
                "04-recommended-route.md",
                "05-human-review-template.yaml",
            ]
            for name in expected:
                self.assertTrue((run_dir / name).exists(), name)

            classification = json.loads((run_dir / "02-classification.json").read_text(encoding="utf-8"))
            self.assertEqual(classification["case_id"], case_id)
            self.assertEqual(classification["primary_capability"], "architecture_analysis")
            self.assertIs(classification["needs_human_review"], True)
            self.assertIs(classification["recommended_destination"]["requires_human_approval"], True)
            self.assertIsNone(classification["recommended_destination"]["suggested_name"])

            request = (input_dir / "request.md").read_text(encoding="utf-8")
            self.assertIn("case-test", request)
            # el runner no debe inventar contexto de negocio ausente en el insumo
            self.assertIn("cliente: por confirmar", request)
            self.assertIn("ambiente: por confirmar", request)
            self.assertIn("Preguntas abiertas", request)

            route = (run_dir / "04-recommended-route.md").read_text(encoding="utf-8")
            self.assertIn("No tocar repos producto", route)
            self.assertIn("El orquestador recomienda", route)
            self.assertNotIn("suggested_name", route)

            facts = (run_dir / "03-facts-and-unknowns.md").read_text(encoding="utf-8")
            self.assertIn("Preguntas abiertas", facts)
            self.assertIn("Supuestos razonables", facts)


if __name__ == "__main__":
    unittest.main()
