import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from Company.baseCompany import BaseCompany
class ViettelCompany(BaseCompany):
    def __init__(self,driver):
        self.driver = driver
    def DownloadFile(self):
        pass
    
    def Login_ViEnvoiceViettel(self,urlLogin,elUserName,elPassWord,xpathelUserName,xpathelPassWord,xpathbtnLogin):
        self.driver.get(urlLogin)
        time.sleep(5)
        self.driver.maximize_window()
        time.sleep(1)
        username = self.driver.find_element(By.XPATH,xpathelUserName)
        username.click()
        time.sleep(1)
        username.send_keys(elUserName)
        time.sleep(1)
        password = self.driver.find_element(By.XPATH,xpathelPassWord)
        password.click()
        time.sleep(1)
        password.send_keys(elPassWord)
        time.sleep(1)
        login = self.driver.find_element(By.XPATH,xpathbtnLogin)
        login.click()
        time.sleep(10)
        self.driver.get('https://vinvoice.viettel.vn/invoice-management/invoice')
        time.sleep(5)
       
    def count_All_item(self):
        count_item_c = self.driver.find_element(By.XPATH,'//*[@id="table"]/div/div[4]/div/jhi-item-count/div').text.split(' ')
        count_item = count_item_c[len(count_item_c)-1]
        return int(count_item)
    
    def click_btn__next(self):
        #//*[@id="table"]/div/div[4]/div/ngb-pagination/ul/li[4]/a
        btn_next_page = self.driver.find_element(By.XPATH,'//*[@id="table"]/div/div[4]/div/ngb-pagination/ul/li[4]/a')
        btn_next_page.click()

    def search_data(self,startDate,endDate):
        btn_mau_hoa_don = self.driver.find_element(By.XPATH,'//*[@id="search"]/div/form/div[1]/div[2]/div/div/ng-select/div/div/div[2]/input')
        btn_mau_hoa_don.click()
        time.sleep(2)
        btn_mau_hoa_don.send_keys(Keys.END)
        time.sleep(1)
        btn_mau_hoa_don.send_keys(Keys.ENTER)
        btn_start_date = self.driver.find_element(By.XPATH,'//*[@id="search"]/div/form/div[2]/div[1]/div/div/div/jhi-app-date-picker[1]/form/div/div/div/input')
        btn_start_date.click()
        btn_start_date.clear()
        time.sleep(2)
        btn_start_date.send_keys(startDate)
        time.sleep(1)
        btn_start_date.send_keys(Keys.ENTER)

        btn_end_date = self.driver.find_element(By.XPATH,'//*[@id="search"]/div/form/div[2]/div[1]/div/div/div/jhi-app-date-picker[2]/form/div/div/div/input')
        btn_end_date.click()
        btn_end_date.clear()
        time.sleep(2)
        btn_end_date.send_keys(endDate)
        time.sleep(1)
        btn_end_date.send_keys(Keys.ENTER)

        #//*[@id="search"]/div/form/div[3]/button[1]/span
        btn_search = self.driver.find_element(By.XPATH,'//*[@id="search"]/div/form/div[3]/button[1]/span')
        btn_search.click()
    
    def check_khong_co_hoa_don(self):
        resul = 0
        try:
            msg = self.driver.find_element(By.XPATH,'//*[@id="invoice-list"]/tbody[2]/tr/td/span').text
            if msg is not None:
                resul = 1
        except Exception as e:
            pass
        return resul
        
    def Action_Main(self,nameFolder,download_folder_c):
        self.dir_sheet_data = self.read_parameter_By_company("vinvoice")
        link = self.dir_sheet_data['link']
        username = self.dir_sheet_data['username']
        password = self.dir_sheet_data['password']
        download_folder = self.dir_sheet_data['download_folder']
        page_size = int(self.dir_sheet_data['page_size'])
        start_date = self.dir_sheet_data['start_date']
        end_date = self.dir_sheet_data['end_date']
        self.Login_ViEnvoiceViettel(link,username,password,'//*[@id="username"]','//*[@id="password"]','/html/body/jhi-main/jhi-login-modal/div/div/div/div[2]/div/div[4]/form/div[4]/button')
        print("Login Vinvoice Viettel Success...")
        time.sleep(10)
        self.create_folder_By_company('/Vinvoice_Viettel_Copany/Old_File')
        self.search_data(start_date,end_date)
        time.sleep(5)
        check_khong_HD = self.check_khong_co_hoa_don()
        if (check_khong_HD == 0):
            print('co hoa don')
            # dem tong so hoa don
            Total_HD = self.count_All_item()
            loop_page = self.countPageSize(page_size,Total_HD)
            mood_page = int(Total_HD % page_size)
            #for page , for item
            if (loop_page == 1):
                self.Download_file(Total_HD,nameFolder,download_folder_c)
            else:
                for i in range(0,loop_page):
                    if(i == loop_page - 1):  
                        self.Download_file(mood_page,nameFolder,download_folder_c)
                    else:
                        self.Download_file(page_size,nameFolder,download_folder_c)
        else:
            print('Khong co Hoa Don trong khoang tim kiem')
       
    def Download_file(self,count_hd,nameFolder,download_folder_c):
        for item in range(0,count_hd):
            print('Download_file',item)
            xpath_btn_dl_x = ''.join(['//*[@id="invoice-list"]/tbody[1]/tr[',str(item + 1),']/td[2]/div/button'])
            btn_i = self.driver.find_element(By.XPATH,xpath_btn_dl_x)
            btn_i.click()
            time.sleep(10)
            btn_tai_zip = self.driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/jhi-invoice-detail/div/div[2]/button[1]/span')
            btn_tai_zip.click()
            time.sleep(15)
            self.get_name_HD(nameFolder,download_folder_c,0,item)
            btn_tai_pdf = self.driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/jhi-invoice-detail/div/div[2]/button[2]/span')
            btn_tai_pdf.click()
            time.sleep(15)
            self.get_name_HD(nameFolder,download_folder_c,1,item)
            time.sleep(3)
            btn_close = self.driver.find_element(By.XPATH,'/html/body/ngb-modal-window/div/div/jhi-invoice-detail/div/div[1]/button/span')
            btn_close.click()
            time.sleep(5)
    
    def get_name_HD(self,nameFolder,download_folder_c,index,id_hd):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'table-responsive'})
        table_body = sup[0].find('table').find_all('tbody')[0]
        trs = table_body.find_all('tr')
        arr_id_tr = []
        name_file = []
        for i,item in enumerate(trs):
                tds = item.find_all('td')
                if len(tds) > 0:
                    name_file.clear()
                    for idx,i in enumerate(tds):
                        match(idx):
                            case 0:
                                stt = i.text
                                name_file.append(stt)
                            case 2:
                                ma_so = i.text.split(' ')[0].split('/')
                                name_file.append(''.join(ma_so))
                            case 3:
                                span = i.find('span').text.split('#')[1]
                                name_file.append(span)
                                small = i.find('small').text.split(' ')[0].split('/')
                                name_file.append(''.join(small))
                            case 13:
                                trang_thai = i.find('span').text
                                name_file.append(trang_thai)
                    arr_id_tr.append('-'.join(name_file))
        for idx,name in enumerate(arr_id_tr):
            if (idx == id_hd):
                name_Old_File = self.get_all_name_file(download_folder_c)
                if (name_Old_File != 0):
                    print('name_Old_File',name_Old_File)
                    file_extension = name_Old_File.split('.')[1]
                    old_name_file = ''.join(['./Output/',nameFolder,'/Vinvoice_Viettel_Copany/Old_File/',name_Old_File])
                    new_name_file = ''.join(['./Output/',nameFolder,'/Vinvoice_Viettel_Copany/',name,'_',str(index),'.',file_extension])
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
                
    
    