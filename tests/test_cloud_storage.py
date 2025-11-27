import os
from pathlib import Path

from bambu_to_prusa.cloud_storage import CLOUD_ROOT_CANDIDATES, detect_cloud_storage_root


def test_detect_cloud_storage_root_prefers_first_candidate(tmp_path):
    # Create two candidate directories to ensure the first match is selected.
    first = tmp_path / CLOUD_ROOT_CANDIDATES[0]
    second = tmp_path / CLOUD_ROOT_CANDIDATES[1]
    first.mkdir()
    second.mkdir()

    detected = detect_cloud_storage_root(home=tmp_path)

    assert detected == first


def test_detect_cloud_storage_root_returns_none_when_missing(tmp_path):
    # Ensure no candidate directories exist.
    for candidate in CLOUD_ROOT_CANDIDATES:
        assert not (tmp_path / candidate).exists()

    assert detect_cloud_storage_root(home=tmp_path) is None
