import os
from re import A

def clean_filename(filename):
	# Split filename and extension
	base_name, ext = os.path.splitext(filename)

	# Remove unwanted substrings from the filename + empty space
	base_name = base_name.replace("(Z-Library)", "").replace("(z-lib.org)", "").rstrip()

	# Return cleaned base name with its extension
	return base_name + ext


def rename_files_in_directory(directory):
	for foldername, subfolders, filenames in os.walk(directory):
		for filename in filenames:
			new_filename = clean_filename(filename)
			if new_filename != filename:
				# Get full paths
				old_file = os.path.join(foldername, filename)
				new_file = os.path.join(foldername, new_filename)
				try:
					# Rename the file
					os.rename(old_file, new_file)
					print(f"Renamed: {old_file} -> {new_file}")
				except Exception as e:
					print(f"Failed to rename {old_file}: {e}")

# Specify the folder where your files are located
root_directory = r"G:\My Drive\Books - epub - pdf"
rename_files_in_directory(root_directory)

# # Sample filenames to test the function
# sample_filenames = [
# 	"Document (Z-library)   .pdf",    # Trailing spaces and (Z-library)
# 	"My Book (z-lib.org)   .txt",     # Trailing spaces and (z-lib.org)
# 	"Test File   .doc",               # Trailing spaces only
# 	"AnotherFile.pdf"                 # No changes expected
# ]

# # Test the function and print results
# for filename in sample_filenames:
# 	print(f"Original: '{filename}' -> Cleaned: '{clean_filename(filename)}'")