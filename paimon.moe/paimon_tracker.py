from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import pyperclip
import time
import subprocess
import shutil

print("Launching Firefox with the --marionette option...")
# Command to launch Firefox with the --marionette option
# command = ["firefox.exe", "--marionette"]
# Execute the command using subprocess
# subprocess.Popen(command)
print("Connecting to the running Firefox instance via Remote WebDriver...")
geckodriver_path = shutil.which("geckodriver.exe")
driver = webdriver.Firefox()
# Connect to the running Firefox instance via Remote WebDriver
print("Connected to Firefox instance.")

print("Execute webdriver service")
# Initialize the Service object with the correct arguments
webdriver_service = Service(executable_path=geckodriver_path, service_args=['--marionette-port', '2828', '--connect-existing'])

print("Setting up the WebDriver...")
# Initialize the WebDriver with the Service object
# driver = webdriver.Firefox(service=webdriver_service)

print("Launching the browser...")
# driver = webdriver.Firefox(service = webdriver_service)
# # options = webdriver.FirefoxOptions()    
# # options.add_argument("-headless")
# driver = webdriver.Firefox(service=firefox_services, options=options)

print("Navigating to 'https://paimon.moe/wish/import'...")
driver.get('https://paimon.moe/wish/import')    
print("Loading Page...")
# Wait for the page to load (you may need to adjust this depending on your internet speed)
time.sleep(2)
    
print("Waiting for the pop-up to appear...")
# Wait for the pop-up to appear and click "Accept" dynamically
WebDriverWait(driver, 10).until(
  EC.element_to_be_clickable((By.CSS_SELECTOR, "button.message-component:nth-child(3)"))
    )
accept_button = driver.find_element(By.CSS_SELECTOR, "button.message-component:nth-child(3)")
accept_button.click()
print("Clicked Accept popup")
    
print("Locating the text box for clipboard content...")
# Locate the text box where you need to paste the clipboard content
text_box = driver.find_element(By.TAG_NAME, 'input')
raw_html = text_box.get_attribute('outerHTML')

print("Running PowerShell command to get clipboard content...")
# PowerShell command you want to run
command = "Import-Module Microsoft.PowerShell.Security; Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex \"&{$((New-Object System.Net.WebClient).DownloadString('https://gist.github.com/MadeBaruna/1d75c1d37d19eca71591ec8a31178235/raw/getlink.ps1'))} global\""

# Run the PowerShell command using subprocess
subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

print("Pasting clipboard content into the text box...")
# Paste the clipboard content into the text box
text_box.click()
text_box.send_keys(pyperclip.paste())

print("Clicking the submit button...")
button = driver.find_element(By.CSS_SELECTOR, ".text-green-400.border-r.border-t-2.border-b-2.border-l-2.border-white.border-opacity-25.rounded-l-xl.px-4.py-2.transition.duration-100")
button.click()

print("Waiting for the page to load...")
# Wait for the page to load (you may need to adjust this depending on your internet speed)
wait = WebDriverWait(driver, 60)
options = (By.CSS_SELECTOR, ".text-green-400.border-2.border-white.border-opacity-25.rounded-xl.px-4.py-2.transition.duration-100")

element = wait.until(EC.element_to_be_clickable(options))
element.click()
print("Clicked the final element.")

print("Pausing until the user presses Enter...")
# Pause until the user presses Enter
time.sleep(5)
input("Press Enter to continue...")
print("Closing the browser...")
# Close the browser
driver.quit()
print("Browser closed.")