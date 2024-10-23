import pytest
from unittest.mock import patch, call
import subprocess
import time
import science_pigeon  # Assuming your script is named science_pigeon.py

@patch('subprocess.run')
def test_download_with_doi(mock_run):
    doi = "10.1000/j.journal.2020.01.001"
    download_dir = r"tests\test_download_folder"
    
    # Call the function or script that triggers the subprocess.run with DOI
    science_pigeon.download_with_doi(doi, download_dir)
    
    mock_run.assert_called_once_with([
        "scidownl", "download",
        "--doi", doi,
        "--out", download_dir
    ])

@patch('subprocess.run')
def test_download_with_title(mock_run):
    clipboard_content = "Some Paper Title"
    download_dir = "/path/to/download"
    
    # Call the function or script that triggers the subprocess.run with title
    science_pigeon.download_with_title(clipboard_content, download_dir)
    
    mock_run.assert_called_once_with([
        "scidownl", "download",
        "--title", clipboard_content,
        "--out", download_dir
    ], check=True)

@patch('subprocess.run')
@patch('science_pigeon.find_pmid_from_title')
def test_download_with_title_error(mock_find_pmid, mock_run):
    clipboard_content = "Some Paper Title"
    download_dir = "/path/to/download"
    pmid = "12345678"
    
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    mock_find_pmid.return_value = pmid
    
    # Call the function or script that triggers the subprocess.run with title and error
    science_pigeon.download_with_title(clipboard_content, download_dir)
    
    mock_run.assert_has_calls([
        call([
            "scidownl", "download",
            "--title", clipboard_content,
            "--out", download_dir
        ], check=True),
        call([
            "scidownl", "download",
            "--pmid", pmid,
            "--out", download_dir
        ])
    ])

if __name__ == "__main__":
    pytest.main()