from __future__ import annotations

import lxml.etree as ET

from .model_processing import DEFAULT_TRANSFORM


def build_prusa_model(objects, template_path: str) -> ET._ElementTree:
    """Inject model objects into the Prusa template and return a tree."""
    tree = ET.parse(template_path)
    model = tree.getroot()
    resources = model.find(".//{*}resources")
    build = model.find(".//{*}build")

    if resources is None or build is None:
        raise ValueError("Template is missing required elements.")

    for object_id, element in objects.items():
        resources.append(element)
        build.append(
            ET.Element(
                "item", objectid=str(object_id), transform=DEFAULT_TRANSFORM, printable="1"
            )
        )

    return tree
