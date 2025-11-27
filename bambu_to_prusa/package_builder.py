from __future__ import annotations

import os
import shutil
from typing import Iterable

import lxml.etree as ET

from .file_ops import compress_zip


def write_model_file(model_tree: ET._ElementTree, filename: str, target_root: str) -> str:
    objects_dir = os.path.join(target_root, "3D", "Objects")
    os.makedirs(objects_dir, exist_ok=True)
    model_path = os.path.join(objects_dir, filename)
    model_tree.write(model_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
    return model_path


def copy_content_types(template_path: str, target_root: str) -> str:
    os.makedirs(target_root, exist_ok=True)
    destination = os.path.join(target_root, "[Content_Types].xml")
    shutil.copy(template_path, destination)
    return destination


def copy_metadata_dir(template_dir: str, target_root: str) -> None:
    metadata_target = os.path.join(target_root, "Metadata")
    if os.path.exists(template_dir):
        os.makedirs(metadata_target, exist_ok=True)
        for file in os.listdir(template_dir):
            shutil.copy(os.path.join(template_dir, file), os.path.join(metadata_target, file))


def generate_relationships(models: Iterable[str], rels_template_path: str, target_root: str) -> str:
    rels_dir = os.path.join(target_root, "_rels")
    os.makedirs(rels_dir, exist_ok=True)

    rels_et = ET.parse(rels_template_path)
    rels_tree = rels_et.getroot()
    relationship_number = 1
    for model in models:
        rel = ET.fromstring(
            f'<Relationship Target="/3D/Objects/{model}" Id="rel-{relationship_number}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/3dmodel"/>'
        )
        relationship_number += 1
        rels_tree.append(rel)

    rels_path = os.path.join(rels_dir, ".rels")
    rels_et.write(rels_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
    return rels_path


def build_package(model_filenames: Iterable[str], template_paths: dict[str, str], target_root: str, output_file: str) -> None:
    copy_content_types(template_paths["content_types_template"], target_root)
    generate_relationships(model_filenames, template_paths["rels_template"], target_root)
    copy_metadata_dir(template_paths["metadata_dir"], target_root)
    compress_zip(target_root, output_file)
