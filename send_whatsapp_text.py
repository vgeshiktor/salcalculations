# whatsapp message
from selenium.webdriver import Keys
from selenium.webdriver.chrome import webdriver

msg = "Hello! I am sending you a file."

# whatsapp contact name
contact = "Inna Sherts"

# path to the file to be sent
file_path = r"C:\Users\innas\Downloads\heskem1.pdf"

# path to the chrome driver
driver_path = r"C:\chromedriver_win32\chromedriver.exe"

# open the whatsapp web page
driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://web.whatsapp.com/")
input("Press Enter after scanning the QR code.")

# find the contact in the search box
search_box = driver.find_element_by_xpath('//div[@title="Search or start new chat"]')
search_box.send_keys(contact)
search_box.send_keys(Keys.ENTER)

# find the input field and send the message
input_field = driver.find_element_by_xpath('//div[@contenteditable="true"]')
input_field.send_keys(msg)

# find the attachment button and click it
attachment_button = driver.find_element_by_xpath('//span[@data-icon="clip"]')
attachment_button.click()

# find the file input field and send the file
file_input = driver.find_element_by_xpath('//input[@accept="*"]')
file_input.send_keys(file_path)

# wait for the file to be sent
input("Press Enter after the file is sent.")

# close the browser
driver.quit()

# # whatsapp message
# from selenium.webdriver import Keys
# from selenium.webdriver.chrome import webdriver
#
# msg = "Hello! I am sending you a file."
#
