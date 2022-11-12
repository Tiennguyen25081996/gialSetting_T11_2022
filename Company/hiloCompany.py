import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Company.baseCompany import BaseCompany
from bs4 import BeautifulSoup
import binascii
import regex as re

class HiloCompany(BaseCompany):
    def __init__(self,driver,path):
        self.driver = driver
        self.path = path
        self.datalistP = []
    def DownloadFileHL(self):
        pass
    def DownloadFile(self,dateFrom,dateTo,status):
        if status == False:
            time.sleep(1)
            QLHD = self.driver.find_elements(By.XPATH,"/html/body/div[1]/div[2]/ul[1]/li[3]/a")[0]
            QLHD.click()
            time.sleep(2)
            DSHD = self.driver.find_elements(By.XPATH,"/html/body/div[1]/div[2]/ul[1]/li[3]/ul/li[2]/a")[0]
            DSHD.click()
        time.sleep(3)
        FromDate = self.driver.find_elements(By.XPATH,"//*[@id='FromDate']")[0]
        FromDate.click()
        time.sleep(1)
        FromDate.clear()
        FromDate.send_keys(dateFrom)
        time.sleep(1)
        ToDate = self.driver.find_elements(By.XPATH,"//*[@id='ToDate']")[0]
        ToDate.click()
        time.sleep(1)
        ToDate.clear()
        ToDate.send_keys(dateTo)
        time.sleep(2)
        SelectStatus = self.driver.find_elements(By.XPATH,"//*[@id='InvoiceStatus']")[0]
        SelectStatus.click()
        # if status == True:
        #     SelectStatus.send_keys(Keys.END)
        #     time.sleep(1)
        #     SelectStatus.send_keys(Keys.ENTER)
        #     time.sleep(2)
        #     btnSearch = self.driver.find_elements(By.XPATH,"/html/body/div[3]/div[2]/div[2]/form/div/div/div/div/div/div[18]/button")[0]
        # else:
        #     SelectStatus.send_keys(Keys.HOME)
        #     time.sleep(1)
        #     SelectStatus.send_keys(Keys.ENTER)
        #     time.sleep(2)
        #     btnSearch = self.driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div[2]/form/div/div/div/div/div/div[18]/button")[0]
        SelectStatus.send_keys(Keys.HOME)
        time.sleep(1)
        SelectStatus.send_keys(Keys.ENTER)
        time.sleep(2)
        btnSearch = self.driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div[2]/form/div/div/div/div/div/div[18]/button")[0]
        btnSearch.click()
        time.sleep(2)

    def VNcode_custom(self,data):
        text = binascii.hexlify(data.encode('cp1258', errors='backslashreplace'))
        return binascii.unhexlify(text).decode('unicode-escape')

    def getCountHD(self):
        soup = BeautifulSoup(self.driver.page_source,features="html.parser")
        countHD = 0
        for item in soup.find('tbody').find_all('tr')[:]:
            tds = item.find_all('td')[:]
            if (len(tds) > 0):
                countHD += 1
                for p in tds:
                    td = p.find_all('p')[:]
                    if (len(td) > 0):
                        for vl_custom in td:
                            if (vl_custom is not None):
                                vl_customs = self.VNcode_custom(str(vl_custom))
                                self.datalistP.append(vl_customs)
        return countHD
    
    
    def Action_Main(self,nameFolder,download_folder_c):
        self.dir_sheet_data = self.read_parameter_By_company('Hilo')
        link = self.dir_sheet_data['link']
        taxcode = self.dir_sheet_data['Taxcode']
        username = self.dir_sheet_data['username']
        password = self.dir_sheet_data['password']
        #download_folder = self.dir_sheet_data['download_folder']
        start_date = self.dir_sheet_data['start_date']
        end_date = self.dir_sheet_data['end_date']
        self.Login(self.driver,link,taxcode,username,password,"//*[@id='taxcode']","//*[@id='username']","//*[@id='password']","//*[@id='btnLogon']")
        print("Login Misa EInvoice Success...")
        time.sleep(10)
        self.create_folder_By_company('/Hilo_Copany/Old_File')
        print("[Start Count HD Err]")
        time.sleep(2)
        self.DownloadFile(start_date,end_date,False)
        time.sleep(2)
        #self.Download_all_file()
        # count all HD
        try:
            c_HD_Success = self.getListHD("body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div:nth-child(1) > div:nth-child(1) > h3")
        except Exception as e:
            print(' Khong Dem Duoc So Hoa Don !!!')
            pass
        if c_HD_Success > 0 :
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source,features="html.parser")
            #c_HD_Success = self.getCountHD()
            soupPSize = soup.select_one('#Pagesize')  
            current_page_size = self.find_current_page_size(soupPSize)
            count_LoopPage = self.countPageSize(current_page_size, c_HD_Success)
            print('count_LoopPage',count_LoopPage)
            print('current_page_size',current_page_size)
            count_hd = self.getCountHD()
            for i in range(0,count_LoopPage):
                if (i == count_LoopPage - 1):
                    count_hd = int(c_HD_Success % current_page_size)

                for item in range(0,count_hd):
                    self.Download_each_file(item,nameFolder,download_folder_c)
                    
                if (i != count_LoopPage - 1):
                    # click next page
                    print('click next page')
                    URL_next = self.getURL_Next_Page()
                    self.next_page(URL_next)
                    time.sleep(8)

            # chup anh man hinh
            time.sleep(2)
            current_url = self.driver.current_url
            new_current_url = current_url.split('page=')[0]
            self.driver.get(''.join([new_current_url,'page=1']))
            time.sleep(8)
            self.Screenshot_all_HD(nameFolder,download_folder_c)
        else:
            print(' Khong co Hoa Don !!!')
    
    def Download_each_file(self,index_current,nameFolder,download_folder_c):
        print("[ Start ] Download HD Active")
        xpath_check_box = ''.join(['/html/body/div[2]/div[2]/div[2]/div[2]/div/div[3]/table/tbody/tr[',str(index_current + 1),']/td[14]/input'])
        check_HD_error = 0
        try:
            self.driver.find_element(By.XPATH,xpath_check_box)
        except Exception as e:
            check_HD_error = 1
            pass
        if check_HD_error == 0:
            time.sleep(2)
            checkbox = self.driver.find_element(By.XPATH,xpath_check_box)
            checkbox.click()
            time.sleep(3)
            btn_downloadHD = self.driver.find_elements(By.CSS_SELECTOR,"body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div:nth-child(2) > div > div:nth-child(2) > button:nth-child(3)")[0]
            btn_downloadHD.click()
            time.sleep(25)
            # popup dowload
            parent_browser = self.driver.current_window_handle
            self.driver.switch_to.default_content
            btn_download = self.driver.find_elements(By.XPATH,"/html/body/div[8]/p/a")[0]
            btn_download.click()
            time.sleep(3)
            btn_Close = self.driver.find_elements(By.XPATH,"/html/body/div[8]/div[7]/button")[0]
            btn_Close.click()
            self.driver.switch_to.window(parent_browser)
            time.sleep(8)
            checkbox = self.driver.find_element(By.XPATH,xpath_check_box)
            time.sleep(3)
            checkbox.click()
            time.sleep(3)
            print("[ Success ] Download HD Active")
            # doi ten file
            time.sleep(8)
            self.get_name_HD(nameFolder,download_folder_c,index_current,False,'')
            # chup anh hoa don
        else:
            print("[ Error ] Hoa Don Bi Huy : ", str(index_current))
     
    def Download_all_file(self):
        print("[ Start ] Download all HD Active")
        ViewHDError = self.driver.find_elements(By.XPATH,"//*[@id='ckbAll']")[0]
        ViewHDError.click()
        time.sleep(5)
        btn_downloadHD = self.driver.find_elements(By.CSS_SELECTOR,"body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div:nth-child(2) > div > div:nth-child(2) > button:nth-child(3)")[0]
        btn_downloadHD.click()
        time.sleep(25)
        # popup dowload
        parent_browser = self.driver.current_window_handle
        self.driver.switch_to.default_content
        btn_download = self.driver.find_elements(By.XPATH,"/html/body/div[8]/p/a")[0]
        btn_download.click()
        time.sleep(5)
        btn_Close = self.driver.find_elements(By.XPATH,"/html/body/div[8]/div[7]/button")[0]
        btn_Close.click()
        self.driver.switch_to.window(parent_browser)
        time.sleep(3)
        print("[ Success ] Download all HD Active") 
    
    def Main_View_All_HD(self,count_LoopPage,cHD,current_page_size,path_custom,name_img_by_company,nameFolder,download_folder_c):
        for item in range(0,count_LoopPage):
            if (item == count_LoopPage-1):
                item_cus = int(cHD % current_page_size)
                print('SO HOA DON PAGE CUOI : ',item_cus)
                URL_next = self.getURL_Next_Page()
                self.next_page(URL_next)
                time.sleep(8)
                self.LoopClickViewAllHD(item_cus,cHD,path_custom,name_img_by_company,nameFolder,download_folder_c)
            elif (item == 0):
                self.LoopClickViewAllHD(current_page_size,cHD,path_custom,name_img_by_company,nameFolder,download_folder_c)
            else:
                URL_next = self.getURL_Next_Page()
                self.next_page(URL_next)
                time.sleep(8)
                self.LoopClickViewAllHD(current_page_size,cHD,path_custom,name_img_by_company,nameFolder,download_folder_c)
    
    def LoopClickViewAllHD(self,in_page_size,c_HD,path,nameCompany,nameFolder,download_folder_c):
        if c_HD < in_page_size :
            loop_hd = c_HD
        else:
            loop_hd = in_page_size
        parent_browser = self.driver.current_window_handle
        z = 0
        if loop_hd == 1:
            z = 0
        else:
            z = 1
        for i in range(z,loop_hd):
            convert_str = str(i)
            name_1st = ''.join([nameCompany,"01",convert_str])
            name_2st = ''.join([nameCompany,"02",convert_str])
            if c_HD == 1:
                zpath_Str = 'body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div.panel-body.table-responsive > table > tbody > tr > td:nth-child(10) > a'
                self.clickViewHDByID(zpath_Str)
                time.sleep(5)
                self.driver.switch_to.default_content
                time.sleep(2)
                element = self.driver.find_elements(By.XPATH,'//*[@id="invoice-footer"]/button[1]')[0]
                time.sleep(8)
                self.Screenshot(self.driver,path + name_1st)
                self.get_name_HD(nameFolder,download_folder_c,i - 1,True,1)
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(8)
                self.Screenshot(self.driver,path + name_2st)
                self.get_name_HD(nameFolder,download_folder_c,i - 1,True,2)
                print("Screenshot success")    
                time.sleep(8)
                element.click()
                time.sleep(3)
                self.driver.switch_to.window(parent_browser)
                time.sleep(2)
                break
            else:
                zpath_Str_1st = 'body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div.panel-body.table-responsive > table > tbody > tr:nth-child('
                zpath_Str_2nd = ') > td:nth-child(10) > a'
                convert_str = str(i)
                zpath_Str = ''.join([zpath_Str_1st,convert_str,zpath_Str_2nd])
            self.clickViewHDByID(zpath_Str)
            time.sleep(5)
            self.driver.switch_to.default_content
            time.sleep(2)
            element = self.driver.find_elements(By.XPATH,'//*[@id="invoice-footer"]/button[1]')[0]
            time.sleep(8)
            self.Screenshot(self.driver,path + name_1st)
            time.sleep(3)
            self.get_name_HD(nameFolder,download_folder_c,i - 1,True,1)
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
            self.Screenshot(self.driver,path + name_2st)
            time.sleep(3)
            self.get_name_HD(nameFolder,download_folder_c,i - 1,True,2)
            print("Screenshot success")    
            time.sleep(5)
            element.click()
            time.sleep(3)
            self.driver.switch_to.window(parent_browser)
            time.sleep(2)
    
    def clickViewHDByID(self,xpath_str):
        el_view = self.driver.find_elements(By.CSS_SELECTOR,xpath_str)[0]
        if el_view is not None:
            el_view.click()
            
    def getListHD(self,xpath):
        try:
            sumHDErr = self.driver.find_elements(By.CSS_SELECTOR,xpath)[0].text
            if sumHDErr is not None:
                countItem = int(sumHDErr.split(':')[1].split(')')[0])
                print(int(countItem))
                return int(countItem)
        except Exception as e:
            print(e)
            return 0
    
    def getURL_Next_Page(self):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'page-a'})
        first_sup = sup[0].find_all('a')
        for item in first_sup:
            print(item.text)
            if (item.text == '>>'):
                return item['href']
            
    def getURL_Back_Page(self):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'page-a'})
        first_sup = sup[0].find_all('a')
        for item in first_sup:
            print(item.text)
            if (item.text == '<<'):
                return item['href']
    
    def next_page(self,qr):
        current_url = self.driver.current_url
        lastest_url = ''
        new_current_url = current_url.split('/EInvoice')[0]
        lastest_url = ''.join([new_current_url,qr])
        print('Next Page :',lastest_url)
        self.driver.get(lastest_url)
    
    def Screenshot_all_HD(self,nameFolder,download_folder_c):
        c_HD_Success = self.getListHD("body > div.page-container.page-navigation-toggled.page-container-wide > div.page-content > div.page-content-wrap.col-lg-12 > div.row > div > div:nth-child(1) > div:nth-child(1) > h3")
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source,features="html.parser")
        #c_HD_Success = self.getCountHD()
        soupPSize = soup.select_one('#Pagesize')  
        current_page_size = self.find_current_page_size(soupPSize)
        count_LoopPage = self.countPageSize(current_page_size, c_HD_Success)
        print('count_LoopPage',count_LoopPage)
        print('current_page_size',current_page_size)
        self.Main_View_All_HD(count_LoopPage,c_HD_Success,current_page_size,self.path,"CommpanyHilo_Success",nameFolder,download_folder_c)  
    
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
    
    def find_current_page_size(self,soupPSize):
        for item in soupPSize.find_all('option', {"selected" : "selected"}):
            return int(item.text)
    
    def get_name_HD(self,nameFolder,download_folder_c,index,check_screenshot,count):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'panel-body table-responsive'})
        table_body = sup[0].find('table').find_all('tbody')[0]

        trs = table_body.find_all('tr')
        print(len(trs))
        print('index get name company : ',index)
        arr_id_tr = []
        for i,item in enumerate(trs):
            if (i == index):
                arr_id_tr.clear()
                tds = item.find_all('td')
                if len(tds) > 0:
                        name_file = []
                        for idx,i in enumerate(tds):
                                    if (idx > 0):
                                        match(idx):
                                            case 1:
                                                text_data = i.text.split('\n')
                                                kyhieu = text_data[2].split(':')[1].split(' ')[1]
                                                name_file.append(kyhieu)  
                                            case 2:
                                                text_data = i.text.split('\n')[1].split(' ')[-1]
                                                so = text_data
                                                name_file.append(so)  
                                            case 5:
                                                arr_date = i.text.split('\n')[1].split(' ')[-1].split('/')
                                                date_data = ''.join(arr_date)
                                                name_file.append(date_data)
                        arr_id_tr.append('_'.join(name_file))
                        
                        
                print('arr_id_tr get name company : ',arr_id_tr)
                
                for name in arr_id_tr:
                    print('name',name)
                    name_Old_File = self.get_all_name_file(download_folder_c)
                    file_extension = name_Old_File.split('.')[1]
                    old_name_file = ''.join(['./Output/',nameFolder,'/Hilo_Copany/Old_File/',name_Old_File])
                    if check_screenshot == True:
                        new_name_file = ''.join(['./Output/',nameFolder,'/Hilo_Copany/',name,'_',str(count),'.',file_extension])
                    else:
                        new_name_file = ''.join(['./Output/',nameFolder,'/Hilo_Copany/',name,'.',file_extension])
                    self.renameFile(old_name_file,new_name_file)