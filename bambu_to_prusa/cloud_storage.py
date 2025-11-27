"""Helpers for locating common cloud storage roots.

This module provides lightweight detection of popular cloud storage
directories so the GUI can offer a sensible default output location.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

# Common cloud storage root folder names. The order reflects typical install precedence.
CLOUD_ROOT_CANDIDATES: tuple[str, ...] = (
    "Dropbox",
    "OneDrive",
    "OneDrive - Personal",
    "Google Drive",
    "iCloud Drive",
)

# Environment variables commonly used by different clients.
ENV_VAR_CANDIDATES: tuple[str, ...] = (
    "OneDriveCommercial",
    "OneDriveConsumer",
    "OneDrive",
    "ONEDRIVE",
    "ONEDRIVE_PATH",
    "DROPBOX_PATH",
    "GOOGLE_DRIVE_PATH",
)


def _existing_path(candidates: Iterable[Path]) -> Path | None:
    for candidate in candidates:
        expanded = candidate.expanduser()
        if expanded.is_dir():
            return expanded
    return None


def detect_cloud_storage_root(home: Path | None = None) -> Path | None:
    """Return a cloud storage directory if common options are found."""

    base_home = home or Path.home()

    env_candidates = [Path(os.environ[var]) for var in ENV_VAR_CANDIDATES if os.environ.get(var)]

    fallback_candidates = [base_home / name for name in CLOUD_ROOT_CANDIDATES]
    onedrive_globs = list(base_home.glob("OneDrive*"))

    icloud_candidates = [
        base_home / "Library" / "Mobile Documents" / "com~apple~CloudDocs",
        base_home / "Library" / "CloudStorage" / "iCloud Drive",
        base_home / "iCloudDrive",
    ]

    return _existing_path([*env_candidates, *fallback_candidates, *onedrive_globs, *icloud_candidates])
