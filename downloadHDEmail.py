from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def set_up_chrome(option):
    option.add_argument("user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data")
    #option.add_experimental_option("debuggerAddress","localhost:9222")
    driver = webdriver.Chrome("chromedriver.exe",options=option)
    return driver
    
if __name__ == '__main__':
    #driver = uc.Chrome(version_main=99)
    #os.open('"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data --remote-debugging-port=9222')
    #driver = webdriver.Chrome(chrome_options=options, executable_path=r"D:\videoYoutube\selenium\chromedriver_win32\chromedriver.exe")
    option = webdriver.ChromeOptions()
    driver = set_up_chrome(option)
    driver.get('https://mail.google.com/mail/u/0/?tab=rm#inbox')
    time.sleep(10)
    search_text = driver.find_elements(By.XPATH,"//*[@id='gs_lc50']/input[1]")[0]
    search_text.click()
    time.sleep(2)
    search_text.send_keys("in:inbox subject:(TPBANK) -in:chats after:2022/7/16 before:2022/7/19")
    time.sleep(2)
    search_text.send_keys(Keys.ENTER)
    time.sleep(10)
    driver.close()