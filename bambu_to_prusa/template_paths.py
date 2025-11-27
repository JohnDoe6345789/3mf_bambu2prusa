from __future__ import annotations

import os
from typing import Dict


def get_template_paths(base_dir: str = "3mf_template") -> Dict[str, str]:
    """Return the template paths relative to the provided base directory."""
    return {
        "models_template": os.path.join(base_dir, "3D", "3dmodel_template.xml"),
        "models_dir": os.path.join(base_dir, "3D"),
        "rels_template": os.path.join(base_dir, "_rels", ".rels_template.xml"),
        "rels_dir": os.path.join(base_dir, "_rels"),
        "content_types_template": os.path.join(base_dir, "[Content_Types].xml"),
        "metadata_dir": os.path.join(base_dir, "Metadata"),
    }
