# Web-scraping-PDF
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

#Dimensions of the webdriver window and scrennshots window
x = 1300
y = 1200
off = 160
#Webdriver install
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
#the webdriver get the Link and Login 
URL = 'https://www.scholarvox.com/reader/docid/88833832/page/1'

username_email = "sarabougrine260@gmail.com"
password_psw = "02022021"
driver.get("https://www.scholarvox.com/login")
username_elements=driver.find_elements_by_xpath("//*[@id='username']")
for username in username_elements:
    try:
        username.send_keys(username_email)
    except Exception as e :
        pass

password_elements=driver.find_elements_by_xpath('//*[@id="password"]')
for psw in password_elements:
    try:
        psw.send_keys(password_psw)
    except Exception as e :
        pass
driver.find_element_by_name("btnsubmit").click()
driver.get(URL)
#create the pdf file 
pdf = FPDF(unit="pt", format=(x - 2 * off + 20, y + 50))
pdf.set_auto_page_break(0)
#take screenshots 
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
