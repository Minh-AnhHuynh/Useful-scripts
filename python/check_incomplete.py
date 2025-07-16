import os
import argparse
import sys
import zipfile
import py7zr


def check_zip(zip_path, extract_dir):
	incomplete_files = []
	with zipfile.ZipFile(zip_path, 'r') as z:
		for zip_info in z.infolist():
			if zip_info.is_dir():
				continue
			target_path = os.path.join(extract_dir, zip_info.filename)
			if os.path.exists(target_path):
				if os.path.getsize(target_path) != zip_info.file_size:
					print(f"Incomplete: {zip_info.filename}")
					incomplete_files.append(zip_info.filename)
			else:
				print(f"Missing: {zip_info.filename}")
				incomplete_files.append(zip_info.filename)
	return incomplete_files


def check_7z(archive_path, extract_dir):
	incomplete_files = []
	with py7zr.SevenZipFile(archive_path, mode='r') as archive:
		for entry in archive.list():
			if entry.is_directory:
				continue
			relative_path = entry.filename
			expected_size = entry.uncompressed
			full_path = os.path.join(extract_dir, relative_path)
			if os.path.exists(full_path):
				if os.path.getsize(full_path) != expected_size:
					print(f"Incomplete: {relative_path}")
					incomplete_files.append(relative_path)
			else:
				print(f"Missing: {relative_path}")
				incomplete_files.append(relative_path)
	return incomplete_files


# Main

parser = argparse.ArgumentParser(
	description="Check incomplete/missing extracted files in zip or 7z archive."
)
parser.add_argument('--archive',
	'-a',
	required=True,
	help="Path to archive file (.zip or .7z)")
parser.add_argument('--dest', '-d', required=True, help="Extraction folder")
parser.add_argument('--output',
	'-o',
	default="incomplete_files.txt",
	help="Output file for missing list")

args = parser.parse_args()

archive_path = args.archive
extract_dir = args.dest

if not os.path.isfile(archive_path):
	print(f"❌ Archive not found: {archive_path}")
	sys.exit(1)
if not os.path.isdir(extract_dir):
	print(f"❌ Extraction folder not found: {extract_dir}")
	sys.exit(1)

ext = os.path.splitext(archive_path)[1].lower()

if args.output == "incomplete_files.txt":
	output_file = os.path.join(os.path.dirname(os.path.abspath(archive_path)),
		"incomplete_files.txt")
else:
	output_file = args.output

if ext == ".zip":
	incomplete_files = check_zip(archive_path, extract_dir)
elif ext == ".7z":
	incomplete_files = check_7z(archive_path, extract_dir)
else:
	print(f"❌ Unsupported archive format: {ext}")
	sys.exit(1)

with open(output_file, "w", encoding="utf-8") as f:
	for file in incomplete_files:
		f.write(f"-i!{file}\n")

print(f"\n✅ Done! {len(incomplete_files)} files need re-extraction.")
print(f"List saved to: {output_file}")
print(
	f'\nTo re-extract, run:\n7z.exe x "{archive_path}" -o"{extract_dir}" -y -i@{output_file}'
)
