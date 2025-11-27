from __future__ import annotations

import os
import re
from typing import Dict

import lxml.etree as ET

MODEL_NAMESPACE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
SLIC3R_NAMESPACE = "http://schemas.slic3r.org/3mf/2017/06"
DEFAULT_TRANSFORM = "0.799151571 0 0 0 0.799151571 0 0 0 0.799151571 184.67373 221.31425 1.61151839"


def read_model_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    with open(path, encoding="utf-8") as file_handle:
        return file_handle.read()


def clean_model_content(content: str) -> str:
    """Remove Bambu specific attributes and normalise namespaces."""
    rem_xmlns = re.sub(r"xmlns=[^\s>]+", "", content)
    rem_puuid = re.sub(r"p:UUID[^\"]+\"[^\"]+\"", "", rem_xmlns)
    rem_encoding = re.sub(r"encoding=[\'\"][\w\d-]+[\'\"]", "", rem_puuid)
    rem_paint_color = rem_encoding.replace("paint_color", "slic3rpe:mmu_segmentation")
    rem_paint_seam = re.sub(r"paint_seam=\"[0-9A-Z]*\"", "", rem_paint_color)
    return re.sub(
        r"<model[ ].*?>",
        f'<model unit="millimeter" xml:lang="en-US" xmlns="{MODEL_NAMESPACE}" xmlns:slic3rpe="{SLIC3R_NAMESPACE}">',
        rem_paint_seam,
    )


def extract_model_objects(clean_xml: str) -> Dict[str, ET._Element]:
    """Return a dictionary of object id to XML element for model objects."""
    bambu_tree = ET.fromstring(clean_xml)
    objects = bambu_tree.findall(".//{*}resources/{*}object")

    relevant_objects: Dict[str, ET._Element] = {}
    for obj in objects:
        if obj.attrib.get("type") == "model":
            relevant_objects[obj.attrib["id"]] = obj
    return relevant_objects


def convert_model_file(path: str) -> tuple[str, Dict[str, ET._Element]]:
    content = read_model_file(path)
    cleaned = clean_model_content(content)
    objects = extract_model_objects(cleaned)
    return os.path.basename(path), objects
