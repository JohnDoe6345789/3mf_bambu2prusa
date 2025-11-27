"""Tests for GUI helpers that don't require a display."""

from bambu_to_prusa_gui import _first_existing_dir


def test_first_existing_dir_returns_first_existing(tmp_path):
    existing = tmp_path / "existing"
    existing.mkdir()

    choice = _first_existing_dir(str(existing), str(tmp_path / "missing"))
    assert choice == str(existing)


def test_first_existing_dir_skips_missing(tmp_path):
    assert _first_existing_dir(str(tmp_path / "missing")) is None
