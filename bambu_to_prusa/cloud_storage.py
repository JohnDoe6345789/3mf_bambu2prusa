"""Cloud storage helpers for picking sensible default paths."""

from pathlib import Path
from typing import Optional

# Common cloud storage root folder names. The order reflects typical install precedence.
CLOUD_ROOT_CANDIDATES = (
    "Dropbox",
    "OneDrive",
    "Google Drive",
    "iCloud Drive",
)


def detect_cloud_storage_root(home: Optional[Path] = None) -> Optional[Path]:
    """Return the first existing cloud storage folder under ``home`` if present.

    A best-effort helper that checks a handful of common providers. If no
    matching directory exists, ``None`` is returned so callers can fall back to
    their default behavior.
    """

    base = home or Path.home()
    for candidate in CLOUD_ROOT_CANDIDATES:
        candidate_path = base / candidate
        if candidate_path.exists():
            return candidate_path
    return None
