"""Helper utilities for frontend implementations."""

import os
from pathlib import Path


def first_existing_dir(*paths: str | os.PathLike[str] | None) -> str | None:
    """Return the first existing directory from the provided paths.
    
    Args:
        *paths: Variable number of path strings or PathLike objects to check
        
    Returns:
        The first existing directory path as a string, or None if none exist
    """
    for path in paths:
        if not path:
            continue
        expanded = Path(path).expanduser()
        if expanded.is_dir():
            return str(expanded)
    return None
