from __future__ import annotations

import os
import shutil
import tempfile
import zipfile


def create_temp_dir(prefix: str = "bambu_to_prusa_") -> str:
    """Create and return a temporary directory path."""
    return tempfile.mkdtemp(prefix=prefix)


def decompress_zip(input_file: str, destination: str | None = None) -> str:
    """Extract *input_file* into *destination* and return the extraction path."""
    if not input_file:
        raise ValueError("Input file path is required for decompression.")

    target_dir = destination or create_temp_dir(prefix="bambu_extract_")
    with zipfile.ZipFile(input_file, "r") as zip_ref:
        zip_ref.extractall(target_dir)
    return target_dir


def compress_zip(source_dir: str, output_file: str) -> None:
    """Zip the contents of *source_dir* into *output_file*."""
    if not source_dir or not output_file:
        raise ValueError("Both source directory and output file are required for compression.")

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zip_out:
        for foldername, _, filenames in os.walk(source_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, source_dir)
                zip_out.write(file_path, arcname)


def cleanup_temp_dir(temp_dir: str | None) -> None:
    """Remove the provided temporary directory if it exists."""
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
