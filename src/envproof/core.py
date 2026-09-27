from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    """A value-safe summary of an environment comparison."""

    missing: tuple[str, ...]
    empty: tuple[str, ...]
    extra: tuple[str, ...]
    duplicates: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not (self.missing or self.empty or self.duplicates)

    def to_dict(self) -> dict[str, object]:
        return {"valid": self.valid, **asdict(self)}


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_env(path: str | Path) -> tuple[dict[str, str], tuple[str, ...]]:
    """Parse a dotenv-like file.

    The parser intentionally handles the common portable subset: comments,
    optional ``export`` prefixes, quoted values, and inline comments after an
    unquoted value. It never interpolates or evaluates content.
    """

    values: dict[str, str] = {}
    duplicates: set[str] = set()
    source = Path(path)

    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            continue

        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key or any(char.isspace() for char in key):
            continue

        value = raw_value.strip()
        if value and value[0] not in {'"', "'"} and " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        value = _unquote(value)

        if key in values:
            duplicates.add(key)
        values[key] = value

    return values, tuple(sorted(duplicates))


def check_environment(
    template_path: str | Path,
    env_path: str | Path,
    *,
    allow_empty: set[str] | None = None,
) -> CheckResult:
    template, _ = parse_env(template_path)
    actual, duplicates = parse_env(env_path)
    allowed = allow_empty or set()

    expected_keys = set(template)
    actual_keys = set(actual)

    return CheckResult(
        missing=tuple(sorted(expected_keys - actual_keys)),
        empty=tuple(
            sorted(key for key in expected_keys & actual_keys if not actual[key] and key not in allowed)
        ),
        extra=tuple(sorted(actual_keys - expected_keys)),
        duplicates=duplicates,
    )
