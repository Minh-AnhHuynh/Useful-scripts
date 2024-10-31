import os
import json
from pathlib import Path
from science_pigeon import get_download_directory

def test_get_download_directory_no_config(monkeypatch, tmp_path):
    # Ensure the config file does not exist
    config_dir = tmp_path / "config"
    config_file_path = config_dir / "pigeon_config.json"
    if config_file_path.exists():
        config_file_path.unlink()

    # Use monkeypatch to set the config path
    monkeypatch.setattr("science_pigeon.config_file_path", config_file_path)

    # Mock input to provide a default download directory
    monkeypatch.setattr("builtins.input", lambda _: str(tmp_path))

    # Test the function
    download_dir = get_download_directory()
    assert download_dir == str(tmp_path) + "\\"

    # Verify that the config file was created with the correct content
    with config_file_path.open("r") as config_file:
        config = json.load(config_file)
        assert config["download_dir"] == str(tmp_path) + "\\"