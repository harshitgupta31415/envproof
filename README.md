# envproof

Validate `.env` files against `.env.example` without printing secret values.

`envproof` catches the configuration mistakes that often surface only after a
deploy: missing keys, accidentally empty values, duplicate declarations, and
undocumented variables. It uses only the Python standard library at runtime.

## Install

```bash
python -m pip install .
```

## Use

```bash
envproof
envproof --template .env.production.example --env .env.production
envproof --strict --allow-empty OPTIONAL_ANALYTICS_ID
envproof --json
```

Example output:

```text
envproof: environment needs attention
  missing: DATABASE_URL
  empty: CLERK_SECRET_KEY
  undocumented (strict): OLD_API_KEY
```

Only key names appear in output. Values are never interpolated, evaluated, or
logged.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Required keys are present and non-empty |
| `1` | Validation failed |
| `2` | A requested file does not exist |

With `--strict`, undocumented keys also make validation fail. JSON output is
suitable for CI pipelines and editor integrations.

## CI integration

Keep a committed `.env.ci` containing non-secret test values, then validate it
against the documented contract before merging:

```yaml
- name: Validate environment contract
  run: envproof --template .env.example --env .env.ci --strict
```

A complete least-privilege GitHub Actions workflow is available in
[`examples/github-actions.yml`](examples/github-actions.yml). Never commit a
production `.env` file merely to validate it in CI.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## License

MIT
