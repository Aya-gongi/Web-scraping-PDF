#!/usr/bin/env python
# coding: utf-8

# In[13]:


import time
from io import BytesIO
from PIL import Image
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
#dimensions of the webdriver and screenshots window
x = 1300
y = 1200
off = 160
#install the webdriver
try:
    print("Drivers initialization")
    edge_options = webdriver.ChromeOptions()
    edge_options.add_argument('--log-level=3')
    edge_options.add_argument('--disable-logging')
    edge_options.add_argument("--headless")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument(F"--window-size={x},{y}")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(10)

except:
    exit("Driver Error")
print("Done !")
#webdriver get the url and login
URL = 'https://www.Link_to_your_book'

username_email = "Email Adress"
password_psw = "Password"
driver.get("https://www.website_of_your_book/login")
username_elements=driver.find_elements_by_xpath("Xpath_of_username_box")
for username in username_elements:
    try:
        username.send_keys(username_email)
    except Exception as e :
        pass

password_elements=driver.find_elements_by_xpath('xpath_of_password_box')
for psw in password_elements:
    try:
        psw.send_keys(password_psw)
    except Exception as e :
        pass
driver.find_element_by_name("name_of_submit_buttom").click()
driver.get(URL)
#create the pdf file and take screenshots
pdf = FPDF(unit="pt", format=(x - 2 * off + 20, y + 50))
pdf.set_auto_page_break(0)
try:
    for i in range(1, 10):
        name = F"page{i}"
        print("Starting " + name)
        driver.get(URL + str(i))
        time.sleep(1.5)
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        output_img = im.crop((off, 0, x - off - 40, y))
        output_img.save(name + ".png")
        pdf.add_page()
        pdf.image(name + ".png")
        print(name.split(".")[0], "done !")
    pdf.output("scraped_book.pdf", "F")
    driver.quit()
except Exception as ignored:
    driver.close()
    driver.quit()


# In[ ]:





# In[ ]:




