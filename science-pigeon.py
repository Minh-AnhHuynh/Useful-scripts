import os
import pyperclip
import subprocess
import re

# Define the download directory
download_dir = "D:\\Library\\Downloads\\Readcube bibliography\\"

# Get the clipboard content
clipboard_content = pyperclip.paste()

# Function to check if the clipboard content is a DOI
def is_doi(content):
	# Check if the content starts with "10." or contains "doi" or "doi.org"
	doi_patterns = [
		r"^10\.",  # Starts with "10."
		r"doi",    # Contains "doi"
		r"doi\.org" # Contains "doi.org"
	]
	return any(re.search(pattern, content, re.IGNORECASE) for pattern in doi_patterns)

# Function to check if the clipboard content is a PMID
def is_pmid(content):
	return content.isdigit()

# Determine if the content is a DOI, PMID, or a title
if is_doi(clipboard_content):
	# Extract the actual DOI if it's part of a URL
	doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", clipboard_content, re.IGNORECASE)
	if doi_match:
		doi = doi_match.group(0)
	else:
		doi = clipboard_content

	# Download using DOI
	subprocess.run([
		"scidownl", "download",
		"--doi", doi,
		"--out", download_dir
	])
elif is_pmid(clipboard_content):
	# Download using PMID
	subprocess.run([
		"scidownl", "download",
		"--pmid", clipboard_content,
		"--out", download_dir
	])
else:
	# Download using title
	subprocess.run([
		"scidownl", "download",
		"--title", clipboard_content,
		"--out", download_dir
	])