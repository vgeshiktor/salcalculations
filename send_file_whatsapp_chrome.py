from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Start a new instance of the Google Chrome driver
driver = webdriver.Chrome(executable_path=r'C:\chromedriver_win32\chromedriver.exe')

# Load the WhatsApp Web page
driver.get("https://web.whatsapp.com/")

# Wait for the user to scan the QR code
input("Press Enter after scanning the QR code.")

# Find the search box and send a message to the desired recipient
search_box = driver.find_element_by_xpath('//div[@title="Search or start new chat"]')
search_box.send_keys("Recipient Name")
search_box.send_keys(Keys.ENTER)

# Find the input field and send the message
input_field = driver.find_element_by_xpath('//div[@contenteditable="true"]')
input_field.send_keys("Hello! I am sending you a file.")

# Find the attachment button and click it
attachment_button = driver.find_element_by_xpath('//span[@data-icon="clip"]')
attachment_button.click()

# Find the file input field and send the file
file_input = driver.find_element_by_xpath('//input[@accept="*"]')
file_input.send_keys("/path/to/file.jpg")

# Wait for the file to be sent
input("Press Enter after the file is sent.")

# Close the browser
driver.quit()
