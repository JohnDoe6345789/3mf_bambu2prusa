"""Helpers for detecting cloud-backed storage folders for output defaults."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable


def _existing_path(candidates: Iterable[Path]) -> Path | None:
    for candidate in candidates:
        expanded = candidate.expanduser()
        if expanded.exists():
            return expanded
    return None


def detect_cloud_storage_root() -> Path | None:
    """Return a cloud storage directory if common options are found."""

    env_candidates = [
        Path(os.environ[var])
        for var in ("OneDriveCommercial", "OneDriveConsumer", "OneDrive")
        if os.environ.get(var)
    ]

    home = Path.home()
    onedrive_globs = home.glob("OneDrive*")

    icloud_candidates = [
        home / "Library" / "Mobile Documents" / "com~apple~CloudDocs",
        home / "Library" / "CloudStorage" / "iCloud Drive",
        home / "iCloudDrive",
    ]

    return _existing_path([*env_candidates, *onedrive_globs, *icloud_candidates])
