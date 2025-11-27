"""Tests for detecting default cloud storage directories."""

from pathlib import Path

import pytest

from bambu_to_prusa.cloud_storage import CLOUD_ROOT_CANDIDATES, detect_cloud_storage_root


@pytest.fixture(autouse=True)
def clear_cloud_env(monkeypatch):
    for key in (
        "OneDrive",
        "OneDriveCommercial",
        "OneDriveConsumer",
        "ONEDRIVE",
        "ONEDRIVE_PATH",
        "DROPBOX_PATH",
        "GOOGLE_DRIVE_PATH",
    ):
        monkeypatch.delenv(key, raising=False)


def test_prefers_onedrive_environment_variable(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    onedrive_dir = tmp_path / "cloud"
    onedrive_dir.mkdir()

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("OneDrive", str(onedrive_dir))

    assert detect_cloud_storage_root(home=home) == onedrive_dir


def test_prefers_dropbox_environment_variable(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    dropbox_dir = tmp_path / "dropbox"
    dropbox_dir.mkdir()

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("DROPBOX_PATH", str(dropbox_dir))

    assert detect_cloud_storage_root(home=home) == dropbox_dir


def test_falls_back_to_icloud_location(tmp_path):
    home = tmp_path / "home"
    cloud_root = home / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
    cloud_root.mkdir(parents=True)

    assert detect_cloud_storage_root(home=home) == cloud_root


def test_favors_first_known_candidate(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    first = home / CLOUD_ROOT_CANDIDATES[0]
    second = home / CLOUD_ROOT_CANDIDATES[1]
    first.mkdir()
    second.mkdir()

    assert detect_cloud_storage_root(home=home) == first


def test_returns_none_when_no_candidates_exist(tmp_path):
    home = tmp_path / "home"
    home.mkdir()

    assert detect_cloud_storage_root(home=home) is None
