import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


compiler = load("compile_prompt", ROOT / "scripts" / "compile-prompt.py")
checker = load("quality_check", ROOT / "scripts" / "quality_check.py")


class ToolTests(unittest.TestCase):
    def test_examples_pass_v3_quality_gate(self):
        for path in (ROOT / "examples").glob("*/SKILL.md"):
            with self.subTest(path=path):
                results = checker.evaluate(path.read_text(encoding="utf-8"))
                self.assertTrue(all(result.passed for result in results), [result for result in results if not result.passed])

    def test_compiler_keeps_v3_content(self):
        source = (ROOT / "examples" / "paul-graham-perspective" / "SKILL.md").read_text(encoding="utf-8")
        prompt = compiler.compile_skill(source)
        self.assertIn("Viaweb", prompt)
        self.assertIn("Do Things That Don't Scale", prompt)
        self.assertGreater(len(prompt), 3000)

    def test_compiler_rejects_incomplete_skill(self):
        with self.assertRaises(ValueError):
            compiler.compile_skill("# Empty\n")


if __name__ == "__main__":
    unittest.main()
