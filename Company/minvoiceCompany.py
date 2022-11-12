import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from Company.baseCompany import BaseCompany
import datetime
import regex as reg


class DatetimeRange:
    def __init__(self, dt1, dt2):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        return self._dt1 < dt < self._dt2


class MinvoiceCompany(BaseCompany):
    def __init__(self,driver):
        self.driver = driver
        self.arr_ky_hieu = []
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
    
    def get_date_time_HD(self,str_date):
        text_split = str_date.split('/')
        day_c = int(text_split[0])
        month_c = int(text_split[1])
        year_c = int(text_split[2])
        return datetime.date(year=year_c, month=month_c, day=day_c)
    
    def check_time_in_range(self,current_date,start,end):
        current = self.get_date_time_HD(current_date)
        start_d = self.get_date_time_HD(start)
        end_d = self.get_date_time_HD(end)
        check = DatetimeRange(start_d, end_d)
        return check.__contains__(current)
    
    def get_id_table_tblDasInvoice(self):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'webix_view webix_dtable mcls_invoiceDashboard','view_id':'tblDasInvoice'})
        table_id = sup[0].get('id')
        return table_id
    
    def click_drop_box_ky_hieu(self):
        sup_ky_hieu_box = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'view_id':'kyhieu_id'})
        box_ky_hieu_id = sup_ky_hieu_box[0].find_all('input')[0].get('id')
        xpath = ''.join(['//*[@id="',box_ky_hieu_id,'"]'])
        self.driver.find_element(By.XPATH,xpath).click()
        time.sleep(2)
    
    def get_array_ky_hieu(self,text_ky_hieu):
        arr_ky_hieu = []
        sup_ky_hieu_box = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'view_id':'kyhieu_id'})
        box_ky_hieu_id = sup_ky_hieu_box[0].find_all('input')[0].get('id')
        btn_drop_box_ky_hieu = self.driver.find_element(By.XPATH,'//*[@id="'+box_ky_hieu_id+'"]')
        btn_drop_box_ky_hieu.click()
        time.sleep(1)
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'webix_view webix_list','role':'listbox'})
        for item in sup:
            list_div_ky_hieu = item.find_all('div',{'class':'webix_list_item'})
            for i in list_div_ky_hieu:
                if reg.search(text_ky_hieu, str(i.text).upper()):
                    arr_ky_hieu.append(i.text)
        return arr_ky_hieu
    
    def get_count_all_item(self):
        sup_page_size = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'view_id':'pagerA','class':'webix_view webix_pager'})
        count_item = sup_page_size[0].text.split(' ')[2].split('.')[0]
        return int(count_item)
    
    def get_data_table_invoiceViews_id(self):
        sup_data_table = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'view_id':'invoiceViews'})
        data_table_id = sup_data_table[0].get('id')
        return data_table_id
    
    def check_khong_co_dl(self):
        data_table_id = self.get_data_table_invoiceViews_id()
        res = 0
        try:
            xpath = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[4]/div'])
            text_C =self.driver.find_element(By.XPATH,xpath).text
            if (text_C == 'Không có dữ liệu'):
                res = 1
        except Exception as e:
            pass
        return res
    
    def click_ky_hieu(self):
        id = self.get_id_table_tblDasInvoice()
        xpath = ''.join(['//*[@id="',id,'"]/div[2]/div[2]/div/div[1]/div/a'])
        self.driver.find_element(By.XPATH,xpath).click()
        time.sleep(5)
        
    def get_all_ky_hieu(self):
        pass
    
    def click_xem_hd(self):
        current_driver = self.driver.current_window_handle
        btn_print = self.driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div[2]/div/div/div[1]/div[2]/div[6]/div/button/span')
        btn_print.click()
        time.sleep(3)
        new_driver = self.driver.window_handles[1]
        self.driver.switch_to.window(new_driver)
        time.sleep(2)
        self.driver.close()
        self.driver.switch_to.window(current_driver)
        time.sleep(1)
    
    def download_file_pdf(self,total_hd,start_date,end_date,nameFolder,download_folder_c):
        data_table_id = self.get_data_table_invoiceViews_id()
        xpath = ''.join(['//*[@id="',data_table_id,'"]/div[1]/div[2]/table/tbody/tr[3]/td[6]/div/input'])
        count_all_item = total_hd + 1
        for hd in range(1,count_all_item):
            btn_search = self.driver.find_element(By.XPATH,xpath)
            btn_search.clear()
            time.sleep(8)
            btn_search.send_keys(hd)
            time.sleep(5)
            last_row = self.get_count_all_item()
            xpath_last_row_search_id = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[7]/div[',str(last_row),']'])
            xpath_last_row_search_trang_thai = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[3]/div[',str(last_row),']'])
            xpath_last_row_search_ngay_hoa_don = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[5]/div[',str(last_row),']'])
            self.driver.find_element(By.XPATH,xpath_last_row_search_id).click()
            ngay_hoa_don = self.driver.find_element(By.XPATH,xpath_last_row_search_ngay_hoa_don).text
            trang_thai = self.driver.find_element(By.XPATH,xpath_last_row_search_trang_thai).text
            if(trang_thai == 'Đã gửi'):
                trang_thai = 'Da_Duoc_Gui'
            else:
                trang_thai = 'Chua_Duoc_Gui'
            print(self.check_time_in_range(ngay_hoa_don,start_date,end_date))
            if (self.check_time_in_range(ngay_hoa_don,start_date,end_date) == True and trang_thai == 'Da_Duoc_Gui'):
                xpath_last_row_search_ma_so_thue = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[8]/div[',str(last_row),']'])
                xpath_last_row_search_ky_hieu = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[6]/div[',str(last_row),']'])
                xpath_last_row_search_trang_thai = ''.join(['//*[@id="',data_table_id,'"]/div[2]/div[2]/div/div[3]/div[',str(last_row),']'])
                ma_so_thue = self.driver.find_element(By.XPATH,xpath_last_row_search_ma_so_thue).text
                id = self.driver.find_element(By.XPATH,xpath_last_row_search_id).text
                ky_hieu = self.driver.find_element(By.XPATH,xpath_last_row_search_ky_hieu).text
                name_file = '-'.join([id,ma_so_thue,ky_hieu,trang_thai])
                time.sleep(1)
                self.click_xem_hd()
                time.sleep(3)
                self.get_name_HD(nameFolder,download_folder_c,name_file)
    
    def Action_Main(self,nameFolder,download_folder_c):
        self.dir_sheet_data = self.read_parameter_By_company("minvoice")
        link = self.dir_sheet_data['link']
        username = self.dir_sheet_data['username']
        password = self.dir_sheet_data['password']
        text_ky_hieu = self.dir_sheet_data['text_ky_hieu']
        download_folder = self.dir_sheet_data['download_folder']
        Ky_hieu = self.dir_sheet_data['Ky_hieu']
        start_date = self.dir_sheet_data['start_date']
        end_date = self.dir_sheet_data['end_date']
        self.Login_Minvoice(link,username,password,'/html/body/div[4]/div[2]/div[7]/div[2]/div/div[4]/div/input','/html/body/div[4]/div[2]/div[7]/div[2]/div/div[5]/div/input','/html/body/div[4]/div[2]/div[7]/div[2]/div/div[7]/div/button')
        print("Login Minvoce_Copany Success...")
        time.sleep(10)
        self.create_folder_By_company('/Minvoce_Copany/Old_File')
        # click ki hieu
        self.click_ky_hieu()
        # get array ki hieu
        self.arr_ky_hieu = self.get_array_ky_hieu(text_ky_hieu)
        print(self.arr_ky_hieu)
        if (len(self.arr_ky_hieu) > 0):
            for idx,item in enumerate(self.arr_ky_hieu):
                # get all item /html/body/div[14]/div/div[2]/div/div/div[2]
                print("Start Ky Hieu : '",item,"'")
                kyhieu = item.strip()
                if ( kyhieu == Ky_hieu):
                    xpath =  ''.join(['/html/body/div[14]/div/div[2]/div/div/div[',str(idx + 1),']'])
                    print(xpath)
                    btn_ky_hieu = self.driver.find_element(By.XPATH,xpath)
                    btn_ky_hieu.click()
                    time.sleep(1)
                    count_all_item = self.get_count_all_item()
                    self.download_file_pdf(count_all_item,start_date,end_date,nameFolder,download_folder_c)
        else:
            print('Khong tim thay ky hieu')
        
    def get_name_HD(self,nameFolder,download_folder_c,name):
        name_Old_File = self.get_all_name_file(download_folder_c)
        if (name_Old_File != 0):
            print('name_Old_File',name_Old_File)
            file_extension = name_Old_File.split('.')[1]
            old_name_file = ''.join(['./Output/',nameFolder,'/Minvoce_Copany/Old_File/',name_Old_File])
            new_name_file = ''.join(['./Output/',nameFolder,'/Minvoce_Copany/',name,'_','.',file_extension])
            self.renameFile(old_name_file,new_name_file)
        
    def countPageSize(self,number_pagesize, number_HD):
        songuyen = 0
        if (number_HD > number_pagesize):
            c = int(number_HD % number_pagesize) # so du
            songuyen_c = (number_HD - c) / number_pagesize
            if c > 0:
                songuyen = songuyen_c + 1
        else:
            songuyen = 1
        return int(songuyen)