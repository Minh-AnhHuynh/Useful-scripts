# FILE: tests/test_science_pigeon.py
import os
import sys
import json
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from science_pigeon import get_download_directory


def test_get_download_directory(monkeypatch, tmp_path):
	# Create a temporary config directory and file
	config_dir = tmp_path / "config"
	config_dir.mkdir()
	config_file_path = config_dir / "pigeon_config.json"

	# Write a sample config file
	config_data = {"download_dir": str(tmp_path)}
	with config_file_path.open("w") as config_file:
		json.dump(config_data, config_file)

	# Use monkeypatch to set the config path
	monkeypatch.setattr("science_pigeon.config_file_path", config_file_path)

	# Test the function
	download_dir = get_download_directory()
	assert download_dir == str(tmp_path)
 
 
