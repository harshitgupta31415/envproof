# Contributing to envproof

Contributions that improve validation accuracy, cross-platform behaviour, or safe diagnostics are welcome.

## Development workflow

1. Fork the repository and create a focused branch.
2. Install the package with `python -m pip install -e .`.
3. Add or update a test in `tests/` for every behaviour change.
4. Run `python -m unittest discover -s tests -v` before opening a pull request.

Never include real `.env` values in fixtures, screenshots, logs, issues, or pull requests. Test fixtures should use clearly fictional values. Keep runtime dependencies at zero unless a change cannot reasonably be implemented with the standard library.

Pull requests should explain the configuration mistake being detected, the expected exit code, and whether terminal and JSON output change.
