import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from Company.baseCompany import BaseCompany
import datetime
from datetime import date
import regex as re
import os

class EHoaDonCompany(BaseCompany):
    def __init__(self,driver):
        self.driver = driver
        self.arr_ky_hieu = []
        self.current = driver.switch_to.default_content()
        
    def DownloadFile(self):
        pass
    
    def Login_Minvoice(self,urlLogin,elUserName,elPassWord,xpathelUserName,xpathelPassWord,xpathbtnLogin):
        self.driver.get(urlLogin)
        time.sleep(10)
        self.driver.maximize_window()
        time.sleep(1)
        username = self.driver.find_element(By.XPATH,xpathelUserName)
        username.click()
        time.sleep(2)
        username.send_keys(elUserName)
        time.sleep(1)
        password = self.driver.find_element(By.XPATH,xpathelPassWord)
        password.click()
        time.sleep(2)
        password.send_keys(elPassWord)
        time.sleep(1)
        login = self.driver.find_element(By.XPATH,xpathbtnLogin)
        login.click()
        time.sleep(10)
    
    def set_up_search(self):
        btn_ngay_hd = self.driver.find_element(By.XPATH,'//*[@id="body_ddlInvoiceDate_ddlCategory"]')
        btn_ngay_hd.click()
        time.sleep(1)
        btn_ngay_hd.send_keys(Keys.HOME)
        time.sleep(1)
        btn_ngay_hd.send_keys(Keys.ENTER)
        
    def check_time_in_range(self,current_date,start,end):
        text_split_r = current_date.split('/')
        day_c_r = int(text_split_r[0])
        month_c_r = int(text_split_r[1])
        year_c_r = int(text_split_r[2])
        text_split = start.split('/')
        day_c = int(text_split[0])
        month_c = int(text_split[1])
        year_c = int(text_split[2])
        text_split_e = end.split('/')
        day_c_e = int(text_split_e[0])
        month_c_e = int(text_split_e[1])
        year_c_e = int(text_split_e[2])
        return date(year_c, month_c, day_c) < date(year_c_r, month_c_r, day_c_r) < date(year_c_e, month_c_e, day_c_e)

    
    def get_count_all_item(self):
        time.sleep(10)
        sup_page_size = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'gg-table-footer'})
        count_item = sup_page_size[0].text.split(' ')[2].split('.')[0]
        return int(count_item)
    
    def download_file_zip(self,name_folder,start,end):
        arr_hd_pass = self.get_list_data_hd(start,end)
        time.sleep(2)
        current = self.driver.switch_to.default_content()
        btn_ngay_hd = self.driver.find_element(By.XPATH,'//*[@id="body_divMore"]/button')
        btn_ngay_hd.click()
        time.sleep(3)
        btn_print_pdf = self.driver.find_element(By.CSS_SELECTOR,'#body_printConvertion')
        btn_print_pdf.click()
        time.sleep(5)
        #check trong ngay
        self.driver.switch_to.frame(current)
        self.driver.switch_to.frame(1)
        find_date = self.driver.find_element(By.XPATH,'//*[@id="gg-table-2"]/tbody/tr[1]/td[3]/div/table/tbody/tr[2]/td[4]')
        find_date.click()
        length_split = len(find_date.text.split(' '))
        start_date_search = find_date.text.split(' ')[length_split - 3]
        end_date_search = find_date.text.split(' ')[length_split - 1]
        today_date = datetime.datetime.now()
        new_today_date = str(today_date.strftime("%d/%m/%Y"))
        #check = self.check_time_in_range(new_today_date,start_date_search,end_date_search)
        check = False
        if (check == True):
            btn_download_search = self.driver.find_element(By.CSS_SELECTOR,'#gg-table-2 > tbody > tr:nth-child(1) > td:nth-child(4) > div > a > div')
            btn_download_search.click()
        else:
            btn_tao_lan_tai = self.driver.find_element(By.XPATH,'//*[@id="btnInvoiceConvertionNew"]')
            btn_tao_lan_tai.click()
            time.sleep(2)
            btn_radio = self.driver.find_element(By.CSS_SELECTOR,'#rblMethod_1')
            btn_radio.click()
            time.sleep(1)
            btn_download = self.driver.find_element(By.CSS_SELECTOR,'#btnConvertion')
            btn_download.click()
        self.driver.switch_to.frame(current)
        time.sleep(30)
        path_down_load = ''.join(['./Output/',name_folder,'/EHoaDon_Copany/'])
        name_file = self.get_name_file_zip(path_down_load)
        print("name_file",name_file)
        path_to= ''.join([path_down_load,'Old_File/'])
        path_from = ''.join([path_down_load,name_file])
        print("path_from",path_from)
        self.UnZipFile(path_from,path_to)
        print("UnZipFile success")
        time.sleep(3)
        self.removeFile(path_from)
        print("removeFile zip")
        time.sleep(8)
        arr_name = self.get_all_name_file_ehoadhon(path_to)
        for i in arr_hd_pass:
            for item in arr_name:
                check = re.search(i,item)
                if(check):
                    print(item)
                    os.replace(path_to + item,path_down_load+ item)      
        try:
            self.delete_all_file_folder(path_to)
            os.rmdir(path_to)
        except Exception as e:
            pass            

    def get_all_name_file_ehoadhon(self,path):
        arr = os.listdir(path)
        if (len(arr) > 0):
            return arr
        else:
            return 0        
    
    def get_name_file_zip(self,path):
        arr = os.listdir(path)
        if (len(arr) > 0):
            return arr[0]
        else:
            return 0
    
    def get_list_data_hd(self,start,end):
        #self.driver.switch_to.frame(self.current)
        arr_hd_pass = []
        count_item = self.get_count_all_item()
        print(int(count_item))
        for item in range(1,int(count_item) + 1):
            xpath_date = ''.join(['//*[@id="gg-table-1"]/tbody/tr[',str(item),']/td[3]/div'])
            date_c = self.driver.find_element(By.XPATH,xpath_date).text.split('\n')[1]
            check_pass = self.check_time_in_range(""+date_c+"",start,end)
            if (check_pass == True):
                arr_hd_pass.append(self.driver.find_element(By.XPATH,xpath_date).text.split('\n')[0])
        return arr_hd_pass
    
    def Action_Main(self,nameFolder):
        self.dir_sheet_data = self.read_parameter_By_company("ehoadon")
        link = self.dir_sheet_data['link']
        username = self.dir_sheet_data['username']
        password = self.dir_sheet_data['password']
        download_folder = self.dir_sheet_data['download_folder']
        start_date = self.dir_sheet_data['start_date']
        end_date = self.dir_sheet_data['end_date']
        self.Login_Minvoice(link,username,password,'//*[@id="txtUserName"]','//*[@id="txtPassword"]','//*[@id="btnLogin"]')
        print("Login EHoaDon_Copany Success...")
        self.set_up_search()
        self.download_file_zip(nameFolder,start_date,end_date)