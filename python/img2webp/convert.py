import sys
from pathlib import Path
from PIL import Image
import tkinter as tk

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"


def fmt_size(b: int) -> str:
	return f"{b / 1024:.1f} KB"


def get_clipboard() -> str:
	root = tk.Tk()
	root.withdraw()
	text = root.clipboard_get()
	root.destroy()
	return text


def main():
	auto_delete = "-del" in sys.argv

	try:
		clipboard = get_clipboard()
	except Exception:
		print(f"{RED}Clipboard is empty or unreadable.{RESET}")
		input("Press Enter to exit...")
		return

	exts = (".jpg", ".jpeg", ".png")
	lines = [
		Path(p.strip().strip('"')) for p in clipboard.splitlines() if p.strip()
	]

	# If clipboard contains a single folder path, scan it
	if len(lines) == 1 and lines[0].is_dir():
		folder = lines[0]
		print(f"{CYAN}Scanning folder:{RESET} {folder}")
		files = [
			f for f in folder.iterdir()
			if f.suffix.lower() in exts and f.is_file()
		]
	else:
		files = [f for f in lines if f.suffix.lower() in exts and f.exists()]

	if not files:
		print(f"{YELLOW}No valid JPG/PNG paths found.{RESET}")
		input("Press Enter to exit...")
		return

	print(
		f"\n{BOLD}{CYAN}Processing {len(files)} picture{'s' if len(files) != 1 else ''}...{RESET}\n"
	)

	converted, failed, larger = [], [], []

	for f in files:
		out = f.with_suffix(".webp")
		orig_size = f.stat().st_size
		print(f"  {DIM}→{RESET} {f.name}  {DIM}({fmt_size(orig_size)}){RESET}")
		try:
			with Image.open(f) as img:
				img.save(out, "WEBP", lossless=True)
			new_size = out.stat().st_size
			diff = new_size - orig_size
			size_info = f"{fmt_size(orig_size)} → {fmt_size(new_size)}"
			if diff > 0:
				print(
					f"  {YELLOW}⚠  {f.name}  {size_info}  (+{fmt_size(diff)}, WebP is larger){RESET}"
				)
				larger.append(f)
			else:
				print(
					f"  {GREEN}✓  {f.name}  {size_info}  ({fmt_size(-diff)} saved){RESET}"
				)
			converted.append(f)
		except Exception as e:
			failed.append(f)
			print(f"  {RED}✗  {f.name}: {e}{RESET}")

	print(f"\n{BOLD}Converted: {len(converted)}  Failed: {len(failed)}{RESET}")
	if larger:
		print(
			f"{YELLOW}⚠  {len(larger)} file{'s' if len(larger) != 1 else ''} produced a larger WebP:{RESET}"
		)
		for f in larger:
			print(f"   {f.name}")

	if failed:
		print(f"{RED}Failed files:{RESET}")
		for f in failed:
			print(f"  {f}")

	if converted:
		# Files safe to delete: converted and not larger (or auto_delete overrides warning)
		safe = [f for f in converted if f not in larger]
		warned = [f for f in converted if f in larger]

		if auto_delete:
			to_delete = safe  # never auto-delete larger files
			if warned:
				print(f"\n{YELLOW}WebP is larger for {len(warned)} file{'s' if len(warned) != 1 else ''} — deleting WebP and keeping original:{RESET}")
				for f in warned:
					webp = f.with_suffix(".webp")
					webp.unlink()
					print(f"  {YELLOW}Reverted {f.name}  (WebP deleted, original kept){RESET}")
			if to_delete:
				for f in to_delete:
					f.unlink()
					print(f"  {DIM}Deleted {f.name}{RESET}")
		else:
			answer = input("\nDelete originals? [y/N] ").strip().lower()
			if answer == "y":
				for f in safe:
					f.unlink()
					print(f"  {DIM}Deleted {f.name}{RESET}")
				if warned:
					print(
						f"{YELLOW}Skipped deleting {len(warned)} file{'s' if len(warned) != 1 else ''} where WebP is larger.{RESET}"
					)

	input(f"\n{DIM}Press Enter to exit...{RESET}")


if __name__ == "__main__":
	main()
