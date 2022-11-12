import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


from Company.baseCompany import BaseCompany

class MisaEInvoice(BaseCompany):
    def __init__(self,driver):
        self.driver = driver
        self.dir_sheet_data = {}
    def DownloadFile(self):
        pass
    
    def Login_Misa(self,elTaxcode,xpathelTaxcode,elUserName,xpathelUserName,xpathNext,elPassWord,xpathelPassWord,xpathbtnLogin,urlLogin):
        self.driver.get(urlLogin)
        time.sleep(5)
        self.driver.maximize_window()
        taxcode = self.driver.find_element(By.XPATH,xpathelTaxcode)
        taxcode.click()
        time.sleep(1)
        taxcode.send_keys(elTaxcode)
        time.sleep(1)
        username = self.driver.find_element(By.XPATH,xpathelUserName)
        username.click()
        time.sleep(1)
        username.send_keys(elUserName)
        time.sleep(1)
        btn_next = self.driver.find_element(By.XPATH,xpathNext)
        btn_next.click()
        time.sleep(3)
        password = self.driver.find_element(By.XPATH,xpathelPassWord)
        password.click()
        time.sleep(1)
        password.send_keys(elPassWord)
        time.sleep(1)
        login = self.driver.find_element(By.XPATH,xpathbtnLogin)
        login.click()
        time.sleep(10)
        self.driver.get('https://app3.meinvoice.vn/v3/hoa-don')
    
    def get_name_company(self):
        TenCty = self.driver.find_element(By.XPATH,'/html/body/nav/div[2]/div[1]').text
        return TenCty
    
    def count_page_size(self):
        count_item = self.driver.find_element(By.XPATH,'//*[@id="grdSAInvoiceWithCode_info"]').text.split(' ')[2]
        return int(count_item)
    
    def count_All_item(self):
        count_item = self.driver.find_element(By.XPATH,'//*[@id="grdSAInvoiceWithCode_info"]').text.split(' ')[4]
        return int(count_item)
    
    def click_btn__next(self):
        #//*[@id="grdSAInvoiceWithCode_next"]
        btn_next_page = self.driver.find_element(By.XPATH,'//*[@id="grdSAInvoiceWithCode_next"]')
        btn_next_page.click()

    def search_data(self,startDate,endDate):
        self.driver.find_element(By.XPATH,'//*[@id="btnFilterToggle"]').click()
        time.sleep(2)
        # search date from
        btn_date_from = self.driver.find_element(By.XPATH,'//*[@id="datepicker-from"]')
        btn_date_from.click()
        time.sleep(1)
        btn_date_from.send_keys(startDate)
        btn_date_from.send_keys(Keys.TAB)
        time.sleep(3)
        # search date to
        btn_date_to = self.driver.find_element(By.XPATH,'//*[@id="datepicker-to"]')
        btn_date_to.send_keys(endDate)
        btn_date_to.send_keys(Keys.TAB)
        time.sleep(3)
        # trang thai hoa don
        btn_Trang_thai_hoa_don = self.driver.find_element(By.XPATH,'//*[@id="sainvoice-filter-popup"]/form/div[6]/div[1]/span/input')
        btn_Trang_thai_hoa_don.clear()
        btn_Trang_thai_hoa_don.send_keys('Hóa đơn gốc')
        btn_Trang_thai_hoa_don.send_keys(Keys.TAB)
        time.sleep(3)
        # trang thai phat hanh
        btn_Trang_thai_phat_hanh = self.driver.find_element(By.XPATH,'//*[@id="sainvoice-filter-popup"]/form/div[6]/div[2]/span/input')
        btn_Trang_thai_phat_hanh.clear()
        btn_Trang_thai_phat_hanh.send_keys('Đã cấp mã')
        btn_Trang_thai_phat_hanh.send_keys(Keys.TAB)
        time.sleep(3)
        #submit
        btn_submit = self.driver.find_element(By.XPATH,'//*[@id="btnFilter"]')
        btn_submit.click()
        
    def get_all_xpath_tr_check_box(self):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'dataTables_scrollBody'})
        table_body = sup[0].find('table').find_all('tbody')[0]
        trs = table_body.find_all('tr')
        arr_id_tr = []
        if len(trs) > 0:
            for item in trs:
                xpath_tr = ''.join(['//*[@id="',item.get('id'),'"]/td[1]/input'])
                arr_id_tr.append(xpath_tr)
        return arr_id_tr
    
    def get_id_form_main(self):
        sup_c = BeautifulSoup(self.driver.page_source,features="html.parser").find('main',{'id':'body-wrapper'}).find_all('div',{'data-viewurl':'/v3/hoa-don'})
        id_form_main = ''
        if len(sup_c) > 0:
            for item in sup_c:
                id_form_main = item.get('id')
        return id_form_main
    
    def Action_Main(self,nameFolder,download_folder_c):
        self.dir_sheet_data = self.read_parameter_By_company("Misa")
        link = self.dir_sheet_data['link']
        taxcode = self.dir_sheet_data['Taxcode']
        username = self.dir_sheet_data['username']
        password = self.dir_sheet_data['password']
        download_folder = self.dir_sheet_data['download_folder']
        page_size = int(self.dir_sheet_data['page_size'])
        start_date = self.dir_sheet_data['start_date']
        end_date = self.dir_sheet_data['end_date']
        self.Login_Misa(taxcode,'//*[@id="TaxCode"]',username,'//*[@id="UserName"]','//*[@id="btnLogin"]',password,'//*[@id="Password"]','//*[@id="btnLogin"]',link)
        print("Login Misa EInvoice Success...")
        time.sleep(10)
        self.create_folder_By_company('/Misa_Einvoice_Copany/Old_File')
        self.search_data(start_date,end_date)
        time.sleep(8)
        try:
            page_size_current = self.count_page_size()
        except Exception as e:
            print(' Khong Dem Duoc So Hoa Don !!!')
            pass
        count_all_item = self.count_All_item()
        if count_all_item >0 :
            print('Total HD DownLoad : ',count_all_item)
            mode_item = count_all_item % page_size_current
            count_LoopPage = self.countPageSize(page_size_current, count_all_item)
            print('Total Loop page DownLoad : ',count_LoopPage)
            print('Total mode_item DownLoad : ',mode_item)
            arr_xpath_tr_checkbox = []
            for i in range(0,count_LoopPage):
                arr_xpath_tr_checkbox.clear()
                arr_xpath_tr_checkbox = self.get_all_xpath_tr_check_box()
                print('So Hoa Don Download : ',len(arr_xpath_tr_checkbox))
                if len(arr_xpath_tr_checkbox) > 0:
                    for idx,item in enumerate(arr_xpath_tr_checkbox):
                        time.sleep(2)
                        self.driver.find_element(By.XPATH,item).click()
                        time.sleep(1)
                        btn_option = self.driver.find_element(By.XPATH,'//*[@id="invoiceMoreAction"]')
                        btn_option.click()
                        id_form_main = self.get_id_form_main()
                        xpath_btn_dl = ''.join(['//*[@id="',id_form_main,'"]/div/div[3]/div[2]/div/div[2]/div/a[1]'])
                        btn_download = self.driver.find_element(By.XPATH,xpath_btn_dl)
                        btn_download.click()
                        time.sleep(30)
                        self.get_name_HD(nameFolder,download_folder_c,idx)
                        time.sleep(2)
                    self.click_btn__next()
                    time.sleep(8)
        else:
            print(' Khong co Hoa Don !!!')
    
    def get_name_HD(self,nameFolder,download_folder_c,index):
        sup = BeautifulSoup(self.driver.page_source,features="html.parser").find_all('div',{'class':'dataTables_scrollBody'})
        table_body = sup[0].find('table').find_all('tbody')[0]
        trs = table_body.find_all('tr')
        arr_id_tr = []
        for i,item in enumerate(trs):
            if (i == index):
                tds = item.find_all('td')
                if len(tds) > 0:
                    name_file = []
                    for idx,i in enumerate(tds):
                        if (idx > 0):
                            match(idx):
                                case 1:
                                    name_file.append(i.get('title'))
                                case 2:
                                    arr_date = i.get('title').split('/')
                                    date_data = ''.join(arr_date)
                                    name_file.append(date_data)
                                case 5:
                                    str_cus = self.no_accent_vietnamese(i.get('title')).split(' ')
                                    name_file.append(''.join(str_cus))
                                case 6:
                                    name_file.append(i.get('title'))
                    arr_id_tr.append('-'.join(name_file))
        
        for name in arr_id_tr:
            name_Old_File = self.get_all_name_file(download_folder_c)
            file_extension = name_Old_File.split('.')[1]
            old_name_file = ''.join(['./Output/',nameFolder,'/Misa_Einvoice_Copany/Old_File/',name_Old_File])
            new_name_file = ''.join(['./Output/',nameFolder,'/Misa_Einvoice_Copany/',name,'.',file_extension])
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
                
          
            
        