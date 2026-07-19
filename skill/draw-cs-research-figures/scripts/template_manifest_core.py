#!/usr/bin/env python3
"""Shared validation and path helpers for editable figure templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SUPPORTED_FORMATS = {"svg", "drawio", "pptx"}
SUPPORTED_KINDS = {"text", "image", "svg-fragment"}


class ManifestError(ValueError):
    pass


def read_json(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"JSON root must be an object: {path}")
    return data


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(manifest.get("schema_version")) != "1.0":
        errors.append("schema_version must be '1.0'")
    templates = manifest.get("templates")
    if not isinstance(templates, dict) or not templates:
        errors.append("templates must be a non-empty object")
    else:
        unknown = set(templates) - SUPPORTED_FORMATS
        if unknown:
            errors.append(f"unsupported template formats: {', '.join(sorted(unknown))}")
    slots = manifest.get("slots")
    if not isinstance(slots, list) or not slots:
        errors.append("slots must be a non-empty array")
        return errors
    seen: set[str] = set()
    for index, slot in enumerate(slots):
        prefix = f"slots[{index}]"
        if not isinstance(slot, dict):
            errors.append(f"{prefix} must be an object")
            continue
        slot_id = slot.get("id")
        if not isinstance(slot_id, str) or not slot_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif slot_id in seen:
            errors.append(f"duplicate slot id: {slot_id}")
        else:
            seen.add(slot_id)
        if slot.get("kind") not in SUPPORTED_KINDS:
            errors.append(f"{prefix}.kind must be one of {sorted(SUPPORTED_KINDS)}")
        selectors = slot.get("selectors")
        if not isinstance(selectors, dict) or not selectors:
            errors.append(f"{prefix}.selectors must be a non-empty object")
        elif not set(selectors).issubset(SUPPORTED_FORMATS):
            errors.append(f"{prefix}.selectors contains an unsupported format")
    return errors


def load_manifest(path: str | Path) -> tuple[dict[str, Any], Path]:
    manifest_path = Path(path).resolve()
    manifest = read_json(manifest_path)
    errors = validate_manifest(manifest)
    if errors:
        raise ManifestError("invalid template manifest:\n- " + "\n- ".join(errors))
    return manifest, manifest_path.parent


def template_path(manifest: dict[str, Any], base: Path, fmt: str) -> Path:
    entry = manifest["templates"].get(fmt)
    if entry is None:
        raise ManifestError(f"manifest has no {fmt} template")
    value = entry.get("path") if isinstance(entry, dict) else entry
    if not isinstance(value, str) or not value:
        raise ManifestError(f"templates.{fmt} must contain a path")
    path = (base / value).resolve()
    if not path.is_file():
        raise ManifestError(f"template does not exist: {path}")
    return path


def replacement_value(values: dict[str, Any], slot: dict[str, Any]) -> Any:
    if slot["id"] not in values:
        if slot.get("required", False):
            raise ManifestError(f"missing required replacement: {slot['id']}")
        return None
    value = values[slot["id"]]
    if isinstance(value, dict):
        return value.get("value", value.get("path", value.get("text")))
    return value

