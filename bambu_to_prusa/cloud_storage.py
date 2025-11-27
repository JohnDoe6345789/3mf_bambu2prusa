"""Helpers for locating common cloud storage roots.

This module provides lightweight detection of popular cloud storage
directories so the GUI can offer a sensible default output location.
"""

import os
from pathlib import Path
from typing import Iterable, Optional


_COMMON_CLOUD_DIRS: tuple[str, ...] = (
    "Dropbox",
    "Google Drive",
    "OneDrive",
    "OneDrive - Personal",
)


def _first_existing_path(paths: Iterable[Path]) -> Optional[str]:
    for path in paths:
        if path and path.is_dir():
            return str(path)
    return None


def detect_cloud_storage_root() -> Optional[str]:
    """Return a cloud storage root directory if one exists."""

    env_candidates = (
        Path(path)
        for path in (
            os.environ.get("DROPBOX_PATH"),
            os.environ.get("ONEDRIVE"),
            os.environ.get("ONEDRIVE_PATH"),
            os.environ.get("GOOGLE_DRIVE_PATH"),
        )
        if path
    )

    home = Path.home()
    home_candidates = (home / name for name in _COMMON_CLOUD_DIRS)

    return _first_existing_path((*env_candidates, *home_candidates))
