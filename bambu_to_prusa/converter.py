from __future__ import annotations

import logging
import os
from pathlib import Path

from .file_ops import cleanup_temp_dir, create_temp_dir, decompress_zip
from .model_injection import build_prusa_model
from .model_processing import convert_model_file
from .package_builder import build_package, write_model_file
from .template_paths import get_template_paths


class BambuToPrusaConverter:
    """Convert Bambu 3MF archives into Prusa-compatible archives."""

    def __init__(self, template_paths: dict[str, str] | None = None):
        self.template_paths = template_paths or get_template_paths()
        self.temp_dir = create_temp_dir()

    def convert_archive(self, input_file: str, output_file: str) -> str:
        if not input_file or not output_file:
            raise ValueError("Both input and output file paths must be provided.")

        extracted_path = decompress_zip(input_file)
        try:
            models_dir = Path(extracted_path) / "3D" / "Objects"
            bambu_models = list(models_dir.rglob("*.model"))
            if not bambu_models:
                raise FileNotFoundError("No .model files found in the archive.")

            prusa_model_filenames: list[str] = []
            for model_path in bambu_models:
                filename, objects = convert_model_file(str(model_path))
                prusa_tree = build_prusa_model(objects, self.template_paths["models_template"])
                write_model_file(prusa_tree, filename, self.temp_dir)
                prusa_model_filenames.append(filename)

            build_package(prusa_model_filenames, self.template_paths, self.temp_dir, output_file)
            logging.info("Output file created: %s", os.path.basename(output_file))
            return output_file
        finally:
            cleanup_temp_dir(extracted_path)
            cleanup_temp_dir(self.temp_dir)
            self.temp_dir = create_temp_dir()
