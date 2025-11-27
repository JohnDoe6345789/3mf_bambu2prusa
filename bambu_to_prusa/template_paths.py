from __future__ import annotations

import os
from pathlib import Path
from typing import Dict


def _default_template_root() -> str:
    """Return the on-disk path to the bundled 3MF template files."""

    package_root = Path(__file__).resolve().parent
    bundled = package_root / "data" / "3mf_template"
    if bundled.exists():
        return str(bundled)

    # Fallbacks for editable installs where the data directory may sit next to the
    # source tree rather than inside the package directory.
    candidates = (
        package_root.parent / "data" / "3mf_template",
        package_root.parent / "3mf_template",
    )
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError("Unable to locate bundled 3MF templates.")


def get_template_paths(base_dir: str | os.PathLike[str] | None = None) -> Dict[str, str]:
    """Return the template paths relative to the provided base directory."""

    resolved_base = str(Path(base_dir) if base_dir else Path(_default_template_root()))
    return {
        "models_template": os.path.join(resolved_base, "3D", "3dmodel_template.xml"),
        "models_dir": os.path.join(resolved_base, "3D"),
        "rels_template": os.path.join(resolved_base, "_rels", ".rels_template.xml"),
        "rels_dir": os.path.join(resolved_base, "_rels"),
        "content_types_template": os.path.join(resolved_base, "[Content_Types].xml"),
        "metadata_dir": os.path.join(resolved_base, "Metadata"),
    }
