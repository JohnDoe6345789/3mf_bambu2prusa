"""Tests for cloud storage detection helpers."""

from pathlib import Path

from bambu_to_prusa.cloud_storage import detect_cloud_storage_root


def test_detect_cloud_storage_root_prefers_environment(monkeypatch, tmp_path: Path) -> None:
    cloud_dir = tmp_path / "env-cloud"
    cloud_dir.mkdir()

    monkeypatch.setenv("ONEDRIVE", str(cloud_dir))
    monkeypatch.delenv("DROPBOX_PATH", raising=False)
    monkeypatch.delenv("ONEDRIVE_PATH", raising=False)
    monkeypatch.delenv("GOOGLE_DRIVE_PATH", raising=False)

    assert detect_cloud_storage_root() == str(cloud_dir)


def test_detect_cloud_storage_root_checks_common_home_dirs(monkeypatch, tmp_path: Path) -> None:
    cloud_dir = tmp_path / "Dropbox"
    cloud_dir.mkdir()

    monkeypatch.delenv("DROPBOX_PATH", raising=False)
    monkeypatch.delenv("ONEDRIVE", raising=False)
    monkeypatch.delenv("ONEDRIVE_PATH", raising=False)
    monkeypatch.delenv("GOOGLE_DRIVE_PATH", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert detect_cloud_storage_root() == str(cloud_dir)
