import os
import pyperclip
import subprocess
import re
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import time
import json
import sys

# Attempt to display \u2193 in the print console
sys.stdout.reconfigure(encoding='utf-8')

# Define the path to the configuration file
config_dir = "config"
config_file_path = os.path.join(config_dir, "pigeon_config.json")


def get_download_directory():
	# Ensure the config directory exists
	if not os.path.exists(config_dir):
		os.makedirs(config_dir)

	if os.path.exists(config_file_path):
		with open(config_file_path, "r") as config_file:
			config = json.load(config_file)
			return config.get(
				"download_dir",
				"D:\\Library\\Downloads\\Readcube bibliography\\")
	else:
		download_dir = input("Enter the default download directory: ")
		# Ensure the directory ends with a backslash
		if not download_dir.endswith("\\"):
			download_dir += "\\"
		with open(config_file_path, "w") as config_file:
			json.dump({"download_dir": download_dir}, config_file)
		return download_dir


# Get the download directory
download_dir = get_download_directory()

# Get the clipboard content
clipboard_content = pyperclip.paste()

# Test
# download_dir = r"tests\test_download_folder"
# clipboard_content = "18% Efficiency organic solarcells"
# Function to check if the clipboard content is a DOI


def is_doi(content):
	# Check if the content starts with "10." or contains "doi" or "doi.org"
	doi_patterns = [
		r"^10\.",  # Starts with "10."
		r"doi",  # Contains "doi"
	]
	for pattern in doi_patterns:
		if re.search(pattern, content, re.IGNORECASE):
			return True
	return False


# Function to check if the clipboard content is a PMID
def is_pmid(content):
	return content.isdigit()


# Does serum 25-hydroxyvitamin Ddecrease during acute-phase response? A systematic review


def is_link(content):
	# Simple check for a URL
	return re.match(r"https?://", content) is not None


def get_content_type(content):
	if is_doi(content):
		return "doi"
	elif is_pmid(content):
		return "pmid"
	elif is_link(content):
		return "link"
	else:
		return "title"


def find_doi_or_pmid_from_title(title):
	query = title
	pmid_found = None
	pubmed_url = None

	for j in search(query):
		print(f"Checking URL: {j}")
		if "pubmed" in j:
			print("Found PubMed URL")
			pubmed_url = j
			print(f"Checking URL: {pubmed_url}")
			pmid_match = re.search(r"/(\d+)/", pubmed_url)
			if pmid_match:
				print(f"Found PMID: {pmid_match.group(1)}")
				pmid_found = pmid_match.group(1)
			# Go to the pubmed URL and extract the DOI
			response = requests.get(pubmed_url)
			soup = BeautifulSoup(response.content, "html.parser")
			doi_link = soup.find("a",
				class_="id-link",
				href=re.compile(r'doi.org'))
			if doi_link and "href" in doi_link.attrs:
				doi = doi_link["href"]
				print(f"Found DOI: {doi}")
				return doi, pmid_found
	else:
		print("No PubMed URL found")
		return None


def subprocess_doi_pmid_from_title(title):
	print("Finding paper from DOI or PMID...")
	doi_pmid_found = find_doi_or_pmid_from_title(clipboard_content)
	if doi_pmid_found is None:
		print("No DOI or PMID found for the given title. Aborting.")
		time.sleep(5)
		return
	subresult_doi = subprocess.run(
		[
		"scidownl", "download", "--doi", doi_pmid_found[0], "--out",
		download_dir
		],
		capture_output=True,
		text=True,
	)
	# Extract and print the last message
	info_messages = re.findall(r'\[.*\].*', subresult_doi.stderr)
	if info_messages:
		print("Last message:\n", info_messages[-1])

	if not "Successfully download" in subresult_doi.stderr:
		print("Failed to download from DOI. Trying with PMID...")
		subresult_pmid = subprocess.run(
			[
			"scidownl",
			"download",
			"--pmid",
			doi_pmid_found[1],
			"--out",
			download_dir,
			],
			capture_output=True,
			text=True,
		)
		# Extract and print the last message
		info_messages = re.findall(r'\[.*\].*', subresult_doi.stderr)
		if info_messages:
			print("Last message:", info_messages[-1])
	else:
		# Extract the title from stderr
		title_match = re.search(r"'title': '([^']+)'", subresult_doi.stderr)
		title_extract = title_match.group(1) if title_match else "Unknown Title"
		# print(
		# 	f"Paper \033[1m{title_extract}\033[0m found and downloaded successfully to \033[1m{download_dir}\033[0m."
		# )


def run_subprocess_title(command):
	result = subprocess.run(command, capture_output=True, text=True)
	info_messages = re.findall(r'\[.*\].*', result.stderr)
	if result.stderr:
		# Check for specific error patterns in stderr
		if not "Successfully download" in result.stderr:
			print(
				"Scidownload did not find the paper from the title. Trying to find DOI or PMID..."
			)
			# Extract and print the last message
			if info_messages:
				print("Last message:\n", info_messages[-1])
			subprocess_doi_pmid_from_title(clipboard_content)
		else:
			print("Last message:", info_messages[-1])


content_type = get_content_type(clipboard_content)

if content_type == "doi":
	doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", clipboard_content,
		re.IGNORECASE)
	doi = doi_match.group(0) if doi_match else clipboard_content
	subprocess.run(
		["scidownl", "download", "--doi", doi, "--out", download_dir])
elif content_type == "pmid":
	subprocess.run([
		"scidownl", "download", "--pmid", clipboard_content, "--out",
		download_dir
	])
elif content_type == "link":
	# Handle link if necessary, assuming it's a DOI link
	doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", clipboard_content,
		re.IGNORECASE)
	if doi_match:
		doi = doi_match.group(0)
		subprocess.run(
			["scidownl", "download", "--doi", doi, "--out", download_dir])
else:
	run_subprocess_title([
		"scidownl", "download", "--title", clipboard_content, "--out",
		download_dir
	])

time.sleep(5)
