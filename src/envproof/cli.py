from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import CheckResult, check_environment


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="envproof",
        description="Check an environment file against its documented template.",
    )
    parser.add_argument("--template", default=".env.example", help="template file (default: .env.example)")
    parser.add_argument("--env", default=".env", dest="env_file", help="environment file (default: .env)")
    parser.add_argument(
        "--allow-empty",
        action="append",
        default=[],
        metavar="KEY",
        help="allow one expected key to be empty; may be repeated",
    )
    parser.add_argument("--strict", action="store_true", help="also fail when undocumented keys are present")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    return parser


def _render(result: CheckResult, strict: bool) -> str:
    lines = ["envproof: environment is valid" if result.valid else "envproof: environment needs attention"]
    for label, keys in (
        ("missing", result.missing),
        ("empty", result.empty),
        ("duplicate", result.duplicates),
        ("undocumented", result.extra),
    ):
        if keys:
            suffix = " (strict)" if label == "undocumented" and strict else ""
            lines.append(f"  {label}{suffix}: {', '.join(keys)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    template = Path(args.template)
    env_file = Path(args.env_file)

    missing_files = [str(path) for path in (template, env_file) if not path.is_file()]
    if missing_files:
        message = {"valid": False, "error": "file_not_found", "files": missing_files}
        print(json.dumps(message) if args.as_json else f"envproof: file not found: {', '.join(missing_files)}")
        return 2

    result = check_environment(template, env_file, allow_empty=set(args.allow_empty))
    strict_valid = result.valid and (not args.strict or not result.extra)
    if args.as_json:
        payload = result.to_dict()
        payload["valid"] = strict_valid
        print(json.dumps(payload, sort_keys=True))
    else:
        print(_render(result, args.strict))
    return 0 if strict_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
