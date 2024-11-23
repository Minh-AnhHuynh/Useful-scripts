from playwright.sync_api import sync_playwright, BrowserContext, Page
from pathlib import Path
import pyperclip
import time
import subprocess
import shutil
import json
import os
from os.path import exists

# Change working directory to the file root
os.chdir(Path(__file__).parent)


def main():
	print("Launching Firefox with Playwright...")
	with sync_playwright() as p:
		browser = p.firefox.launch(headless=False)
		context = browser.new_context()
		page = context.new_page()
		print("Connected to Firefox instance.")

		print("Navigating to 'https://paimon.moe/wish/import'...")
		page.goto('https://paimon.moe/wish/import')
		print("Loading Page...")
		print("Waiting for the pop-up to appear...")

		def store_cookies(context: BrowserContext):
			cookies = context.cookies()
			Path("paimon_cookies.json").write_text(json.dumps(cookies))
			print("Saved current cookies")

		def load_cookies(context: BrowserContext):
			cookie_path = "paimon_cookies.json"
			if exists(cookie_path):
				cookies = json.loads(Path(cookie_path).read_text())
				context.add_cookies(cookies)
				print("Loaded cookies from file")

		store_cookies(BrowserContext)
		
		print("Locating the text box for clipboard content...")
		# Locate the text box where you need to paste the clipboard content
		text_box = page.query_selector('input')

		# Additional steps
		options = page.query_selector(
			".text-green-400.border-2.border-white.border-opacity-25.rounded-xl.px-4.py-2.transition.duration-100"
		)
		options.click()
		print("Clicked the final element.")

		print("Pausing until the user presses Enter...")
		# Pause until the user presses Enter
		time.sleep(5)
		input("Press Enter to continue...")
		print("Closing the browser...")
		# Close the browser
		browser.close()


print("Running the Playwright script...")
main()
