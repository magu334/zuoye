from __future__ import annotations

from importlib import import_module


_ROOT_MODULES = {
    "audit_dataset",
    "extract_fields",
    "parse_check",
    "parse_docs",
    "report_results",
    "route_sections",
    "validate_results",
}


def __getattr__(name: str):
    if name in _ROOT_MODULES:
        return import_module(name)
    raise AttributeError(name)
