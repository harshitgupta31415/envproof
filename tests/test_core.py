from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from envproof.core import check_environment, parse_env


class EnvProofTests(unittest.TestCase):
    def test_parser_supports_export_quotes_and_inline_comments(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text('export API_URL="https://example.com"\nPORT=3000 # dev\n', encoding="utf-8")
            values, duplicates = parse_env(path)
            self.assertEqual(values, {"API_URL": "https://example.com", "PORT": "3000"})
            self.assertEqual(duplicates, ())

    def test_reports_only_key_names(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / ".env.example"
            actual = root / ".env"
            template.write_text("DATABASE_URL=\nTOKEN=\nOPTIONAL=\n", encoding="utf-8")
            actual.write_text("TOKEN=super-secret\nOPTIONAL=\nEXTRA=value\nTOKEN=rotated\n", encoding="utf-8")

            result = check_environment(template, actual, allow_empty={"OPTIONAL"})

            self.assertEqual(result.missing, ("DATABASE_URL",))
            self.assertEqual(result.extra, ("EXTRA",))
            self.assertEqual(result.duplicates, ("TOKEN",))
            self.assertNotIn("super-secret", str(result))

    def test_empty_required_value_is_invalid(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "template").write_text("A=\n", encoding="utf-8")
            (root / "actual").write_text("A=\n", encoding="utf-8")
            result = check_environment(root / "template", root / "actual")
            self.assertEqual(result.empty, ("A",))
            self.assertFalse(result.valid)


if __name__ == "__main__":
    unittest.main()
