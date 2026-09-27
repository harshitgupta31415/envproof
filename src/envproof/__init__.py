"""Environment-file validation without secret disclosure."""

from .core import CheckResult, check_environment, parse_env

__all__ = ["CheckResult", "check_environment", "parse_env"]
__version__ = "0.1.0"
