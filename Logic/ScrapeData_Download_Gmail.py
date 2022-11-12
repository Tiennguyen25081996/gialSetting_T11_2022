from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import re
from datetime import datetime
import regex as re
import os


from Logic.downloadHD import DownloadHD
#python -m pip install beautifulsoup4
class ScrapDataWeb_Download_Gmail:
    def __init__(self,namecompany,host,username,password,download_folder):
        self.NameCompany = namecompany
        self.host = host
        self.username = username
        self.password = password
        self.download_folder = download_folder
        self.ojb_downloadHD = DownloadHD()
    
    count_Email = 0
    arr_id_files_dl = []
    Total_email = []
    loop_all_page = 0
    mood_email_loop = 0
    arr_id_tr_span = []
    
    def log_In_Gmail(self,driver):
        time.sleep(5)
        element_User_name = driver.find_elements(By.XPATH,'//*[@id="identifierId"]')[0]
        element_User_name.click()
        time.sleep(1)
        element_User_name.send_keys(self.username)
        element_User_name.send_keys(Keys.ENTER)
        time.sleep(5)
        element_pass = driver.find_elements(By.CSS_SELECTOR,'#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')[0]
        element_pass.click()
        time.sleep(1)
        element_pass.send_keys(self.password)
        element_pass.send_keys(Keys.ENTER)
        time.sleep(10)
    
    def click_by_id(self,d,i):
        time.sleep(1)
        print(str(i))
        btn_d = d.find_elements(By.ID,str(i))[0]
        btn_d.click()
        time.sleep(1)

    def get_id_el_download_file(self,driver):
        self.arr_id_files_dl.clear()
        soup_by_email = BeautifulSoup(driver.page_source,features="html.parser")
        div_dinh_kem = soup_by_email.find_all('div',{"role":"button",'data-tooltip':'Tải xuống'})
        for item in div_dinh_kem:
            id = item.get('id')
            if id is not None :
                self.arr_id_files_dl.append(id)
                
    def get_loop_mod_page_email(self,count_all_email,page_size_cus):
        loop_all_page = 0 
        mood_email_loop= 0
        page_size_cus_int = int(page_size_cus)
        if count_all_email >= page_size_cus_int:
            mood_email_loop = count_all_email % page_size_cus_int
            print('mood_email_loop',mood_email_loop)
            count_email = count_all_email - mood_email_loop
            loop_all_page = int( count_email / page_size_cus_int)
            if mood_email_loop > 0 :
                loop_all_page += 1
        else:
            loop_all_page = 1
        print('loop_all_page',loop_all_page)
        return loop_all_page,mood_email_loop
    
    def click_all_next_page(self,driver,link_output, name_file_log_success,count):
        for item in range(0,count):
            time.sleep(3)
            self.click_next_page_search(driver,link_output,name_file_log_success)
            
    def count_all_email_page_1st(self,driver):
        self.Total_email.clear()
        soup = BeautifulSoup(driver.page_source,features="html.parser")
        get_span_dj = soup.find('span',{'class','Dj'})
        count_span = len(get_span_dj)
        if count_span > 0:
            for item in get_span_dj:
                self.Total_email.append(item.text)
        else:
            print('Cant Find Total Email')
        return int(self.Total_email[-1])
            
    def count_all_email(self,driver):
        self.Total_email.clear()
        soup = BeautifulSoup(driver.page_source,features="html.parser")
        get_span_dj = soup.find('div',{'class':'D E G-atb PY','gh':'tm'}).find_all('span',{'class':'Dj'})
        #get_span_dj = soup.find('span',{'class','Dj'})
        count_span = len(get_span_dj)
        if count_span > 0:
            for item in get_span_dj:
                self.Total_email.append(item.text.split(' ')[-1])
        else:
            print('Cant Find Total Email')
        return int(self.Total_email[-1])

    def get_id_tr_span_arr(self,driver):
        self.arr_id_tr_span.clear()
        soup = BeautifulSoup(driver.page_source,features="html.parser")
        div_table = soup.find('div',{"class":"AO"}).find_all('div',{"class":"Cp"})
            
        for tb in div_table:
            check_ha_table = tb.find('table')
            if check_ha_table is not None:
                if (tb == div_table[-1]):
                    try:
                        tbs = tb.find('table').find_all('tr')
                        if(len(tbs)==0):
                            break
                        for trc in tbs:
                            tds = trc.find_all('td',{'role':'gridcell'})
                            for td in tds:
                                td_c = td.get('id')
                                if (td_c is not None):
                                    spans = td.find_all('span',{'class':'bog'})
                                    for spa in spans:
                                        id_spa = spa.get('id')
                                        if (id_spa is not None):
                                            self.arr_id_tr_span.append(id_spa)
                    except print(0):
                        pass    

    def get_title_EmailKT(self,driver):
        soup_ha = BeautifulSoup(driver.page_source,features="html.parser")
        tieudes = soup_ha.find_all('div',{"class":"ha"})
        for item in tieudes:
            h2_tag = item.find('h2')
            if h2_tag is not None :
                return h2_tag.text
            
    def get_all_html_page_source(self,driver):
        soup_ha_1 = BeautifulSoup(driver.page_source,features="html.parser")
        # kill all script and style elements

        for script in soup_ha_1(["script", "style"]):
            script.extract()    # rip it out

        # get text

        text = soup_ha_1.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def Write_Log(self,pathfile,namefile,text):
        # now = datetime.now() # current date and time
        # date_time_Folder = now.strftime("%m%d%Y")
        sentence = text.strip()
        sentence = self.ojb_downloadHD.chuan_hoa_dau_cau_tieng_viet(sentence)
        f = open(pathfile + '\\' + namefile + "_log.txt", "a", encoding='utf8')
        f.write(sentence +"\n")
        f.close()

    def get_name_foldel(self):
        now = datetime.now() # current date and time
        date_time_Folder = now.strftime("%m%d%Y")
        return date_time_Folder
    
    def check_map_email_HDDT(self,arr_title_HDDT_c,title_curent_email):
        check = 0
        for item in arr_title_HDDT_c:
            item_upper = item.upper()
            if re.search(item_upper,title_curent_email):
                check = 1
                return check
        return check
    
    def search_email_by_date(self,driver,start_date,end_date):
        sql_c = ''.join(['after:',start_date,'before:',end_date])
        search_text = driver.find_elements(By.CSS_SELECTOR,'#gs_lc50 > input:nth-child(1)')[0]
        search_text.click()
        time.sleep(4)
        search_text.send_keys(sql_c)
        time.sleep(2)
        search_text.send_keys(Keys.ENTER)
 
    def check_map_link_download_HDDT(self,arr_title_HDDT_c,title_curent_email,download_folder_c):
        check = 0
        for item in arr_title_HDDT_c:
            if re.search(item,title_curent_email):
                match item:
                    case 'tracuuhoadon.hc.com.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web tracuuhoadon.hc.com.vn tải thành công')
                        check = 1
                        break 
                    case 'tracuu.ehoadon.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web tracuu.ehoadon.vn tải thành công')
                        check = 2
                        break
                    case 'hd.easyinvoice.com.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web hd.easyinvoice.com.vn tải thành công')
                        check = 3
                        break
                    case 'hddt.digiworld.com.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web hddt.digiworld.com.vn tải thành công')
                        check = 4
                        break   
                    case 'www.xuathoadon.com.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web www.xuathoadon.com.vn tải thành công')
                        check = 5
                        break  
                    case 'cadmin-group1.mifi.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web cadmin-group1.mifi.vn tải thành công')
                        check = 6
                        break
                    case 'portaltool-mienbac.vnpt-invoice.com.vn':
                        self.Write_Log(download_folder_c,'ThinkAndDo', 'mở web portaltool-mienbac.vnpt-invoice.com.vn tải thành công')
                        check = 7
                        break        
                    case default:#tracuu.smartcom.com.vn
                        self.Write_Log(download_folder_c,'ThinkAndDo','[WARNING]Web hiện tại chưa training cho bot \n')
                        self.Write_Log(download_folder_c,'ThinkAndDo','[WARNING]Web là : ' + str(item))
                        break
        return check

    def get_link_download_file_pdf(self,driver,arr_content_HDDT,arr_title_HDDT):
        link_c = ''
        array_loai4 = []
        page_source_c = BeautifulSoup(driver.page_source,features="html.parser")
        #arr_content_HDDT_c = ['Tra cứu tại','Để tải hóa đơn PDF','Để tải trực tiếp hóa đơn dạng PDF','Để tra cứu hóa đơn truy cập địa chỉ:','Quý khách vui lòng truy cập','Quý khách đã được phát hành với Mã tra cứu là','Để tải hóa đơn dạng PDF','Để tải hóa đơn dạng pdf']
        title_curent_email = self.get_title_EmailKT(driver)
        #print(title_curent_email.upper())
        check = self.check_map_email_HDDT(arr_title_HDDT,title_curent_email.upper())
        content_page_html  = self.get_all_html_page_source(driver)
        id_content = len(content_page_html.split(title_curent_email)) - 1
        #print('==============================================================')
        content_page = content_page_html.split(title_curent_email)[id_content]
        #print(content_page_html.split(title_curent_email)[id_content])
        for item in arr_content_HDDT:
            check_c = self.check_map_email_HDDT(content_page,item.upper())
            if (check_c == 1):
                xpath_C = ''.join(["//*[contains(text(), '",item,"')]"])
                x_el = driver.find_elements(By.XPATH,xpath_C)
                if len(x_el) > 0:
                    for i in x_el:
                        i_search = ''.join([item,'*'])
                        all_tag_c = page_source_c.find(text=re.compile(i_search))
                        if (item == 'Để tra cứu hóa đơn truy cập địa chỉ:' or item == 'Để tải hóa đơn dạng pdf'):
                            #print(item)
                            all_tag_a = all_tag_c.find_next('a')
                            print('loai 2 : ',all_tag_a.get('data-saferedirecturl'))
                            link_c = all_tag_a.get('data-saferedirecturl')
                            return link_c
                        elif (item == 'Quý khách đã được phát hành với Mã tra cứu là'):
                            all_tag_a = all_tag_c.find_next('a')
                            if len(all_tag_a) > 0:
                                print('loai 3 : ',all_tag_a.get('data-saferedirecturl'))
                                link_c = all_tag_a.get('data-saferedirecturl')
                                return link_c
                        else:
                            #print(item)
                            all_tag_a = all_tag_c.find_next_siblings('a')
                            last_item = len(all_tag_a) - 1
                            if len(all_tag_a) > 0:
                                link_c_item = ''
                                link_c_item = all_tag_a[last_item].get('data-saferedirecturl')
                                array_loai4.append(link_c_item)
                    if len(array_loai4) > 0:
                        link_c = array_loai4[0]
                        print('loai 4 : ',all_tag_a[last_item].get('data-saferedirecturl'))
                        return link_c

    def setUp_Driver(self,download_folder_c):
        # option = webdriver.ChromeOptions()
        # option.add_argument("--disable-blink-features=AutomationControlled")
        # option.add_argument('ignore-certificate-errors')
        # option.add_argument("--start-maximized")
        # option.add_argument("--disable-web-security")
        # option.add_argument("--allow-running-insecure-content")
        # option.add_argument('--disable-gpu')
        # option.add_argument('--disable-software-rasterizer')
        # option.add_argument("--safebrowsing-disable-extension-blacklist")
        # option.add_argument('--safebrowsing-disable-download-protection')
        # option.add_argument("--disable-extensions")
        # option.add_experimental_option("excludeSwitches", ["enable-automation"])
        # option.add_experimental_option("useAutomationExtension", False)
        # prefs = {'download.directory_upgrade': True,"download.default_directory" : download_folder,'download.prompt_for_download': 'false','download.extensions_to_open': 'xml','safebrowsing.enabled': 'true'}
        # option.add_experimental_option("prefs",prefs)
        # driver = webdriver.Chrome("chromedriver.exe",options=option)
        option = webdriver.ChromeOptions()
        #option.add_argument("user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data")
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_argument("no-sandbox")
        option.add_argument("--disable-gpu")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--disable-notifications")
        option.add_experimental_option("useAutomationExtension", False)
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome("chromedriver.exe",options=option)
        # code fix download file xml
        print('set up driver : ',download_folder_c)
        params = {'behavior' : 'allow', 'downloadPath': download_folder_c}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
        # params = {'behavior' : 'allow', 'downloadPath': download_folder}
        # driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
        return driver
    
    def CreateFolderByPath(self,path):
        newpath = path
        print("Create Name Folder : ",newpath)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        return newpath
    
    def CreateFolderByTime(self,path):
        now = datetime.now() # current date and time
        date_time_Folder = now.strftime("%m%d%Y")
        newpath = path + date_time_Folder
        print("Create Name Folder : ",newpath)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        return newpath
    
    def click_next_page_search(self,driver,link_output,name_file_log_err):
        page_source_c = BeautifulSoup(driver.page_source,features="html.parser")
        time.sleep(2)
        id_div_next_pages = page_source_c.find('div',{'class':'D E G-atb PY','gh':'tm'}).find_all('div',{'data-tooltip':'Cũ hơn'})[0]
        if (len(id_div_next_pages) > 0):
            id_div_next_page = id_div_next_pages.get('id')
        print('next page ID : ',id_div_next_page)
        if (id_div_next_page is not None):
            driver.find_element(By.ID,id_div_next_page).click()
        else:
            self.Write_Log(link_output,name_file_log_err,'[ERROR] Không tìm thấy button next page.')
    
    def click_next_page(self,driver,link_output,name_file_log_err):
        page_source_c = BeautifulSoup(driver.page_source,features="html.parser")
        time.sleep(2)
        id_div_next_pages = page_source_c.find('span',{'class':'Di'}).find_all('div',{'data-tooltip':'Cũ hơn'})[0]
        if (len(id_div_next_pages) > 0):
            id_div_next_page = id_div_next_pages.get('id')
        print('next page ID : ',id_div_next_page)
        if (id_div_next_page is not None):
            driver.find_element(By.ID,id_div_next_page).click()
        else:
            self.Write_Log(link_output,name_file_log_err,'[ERROR] Không tìm thấy button next page.')
    
    def Auto_click_download_each_email(self,driver,arr_title_HDDT,arr_content_HDDT_c,arr_web_open_by_link,link_output,name_file_log_err,name_file_log_success,loop_all_page):
        # check_next_page = 0
        idx_email_select_in_page = 0
        # current_page = 0
        for lp in range(0,loop_all_page):
            # current_page = lp
            self.Write_Log(link_output,name_file_log_success, '**************************************************************************************************************************')
            self.Write_Log(link_output,name_file_log_success, '************************************************** Page ' + str(lp) + ' **************************************************')
            if lp != 0:
                self.click_next_page_search(driver,link_output,name_file_log_err)
                time.sleep(3)
                self.get_id_tr_span_arr(driver)

            for idx,item in enumerate(self.arr_id_tr_span):
                self.Write_Log(link_output,name_file_log_success, '======================================== Email index : ' + str(idx) + ' ==============================================')
                # check_next_page = 0
                if (idx_email_select_in_page == idx):
                    driver.find_elements(By.ID,item)[0].click()
                    print('ID Tr click : ',item)
                    time.sleep(3)
                    title_email = self.get_title_EmailKT(driver)
                    check = self.check_map_email_HDDT(arr_title_HDDT,title_email.upper())
                    time.sleep(1)
                    if check == 1:
                        self.get_id_el_download_file(driver)
                        
                        time.sleep(2)
                        # check co file dinh kem
                        if len(self.arr_id_files_dl) > 0:
                            print(self.arr_id_files_dl)
                            self.Write_Log(link_output,name_file_log_success, 'Tổng file đính kèm là : '+ str(len(self.arr_id_files_dl)))
                            self.Write_Log(link_output,name_file_log_success, 'Loại 1 : '+ title_email)
                            time.sleep(1)
                            for idx,item in enumerate(self.arr_id_files_dl):
                                time.sleep(2)
                                self.click_by_id(driver,item)
                                time.sleep(3)
                        else:
                            # khong co file dinh kem
                            # get value content email
                            soup_content_email = BeautifulSoup(driver.page_source,features="html.parser")
                            gmail_gs_content = soup_content_email.find('div',{'class':'gs'})
                            self.Write_Log(link_output,name_file_log_success, 'Không thấy file đính kèm nên sẽ tìm link download file pdf')
                            if len(gmail_gs_content) > 0:
                                time.sleep(1)
                                link_text = self.get_link_download_file_pdf(driver,arr_content_HDDT_c,arr_title_HDDT)
                                if (link_text is not None):
                                    self.Write_Log(link_output,name_file_log_success, 'Đã tìm thấy link tải file pdf. \n')
                                    self.Write_Log(link_output,name_file_log_success, 'Link tải PDF là : '+ str(link_text))
                                    time.sleep(1)
                                    check_link_text = self.check_map_link_download_HDDT(arr_web_open_by_link,link_text,link_output)
                                    if (check_link_text == 1):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'Web tracuuhoadon.hc.com.vn \n')
                                        current_driver = driver.current_window_handle
                                        self.Write_Log(link_output,name_file_log_success, title_email)
                                        driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div/div[1]/div[2]/div[6]/div/button').click()
                                        time.sleep(4)
                                        driver.back()
                                        driver.switch_to.window(current_driver)
                                        time.sleep(3)
                                    elif (check_link_text == 2):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'Web tracuu.ehoadon.vn \n')
                                        current_driver = driver.current_window_handle
                                        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR,'#frameViewInvoice'))
                                        driver.find_element(By.ID,'btnDownload').click()
                                        time.sleep(1)
                                        driver.find_element(By.ID,'LinkDownPDF').click()
                                        time.sleep(4)
                                        driver.back()
                                        driver.switch_to.window(current_driver)
                                        time.sleep(3)
                                    elif (check_link_text == 3):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'Web hd.easyinvoice.com.vn \n')
                                        time.sleep(5)
                                        driver.back()
                                    elif (check_link_text == 4):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'Web hddt.digiworld.com.vn \n')
                                        time.sleep(4)
                                        driver.back()
                                    elif (check_link_text == 5):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'Web www.xuathoadon.com.vn \n')
                                        time.sleep(12)
                                        #driver.back()
                                    elif (check_link_text == 6):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'cadmin-group1.mifi.vn \n')
                                        time.sleep(4)
                                        driver.back()
                                    elif (check_link_text == 7):
                                        driver.get(link_text)
                                        time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_success, 'portaltool-mienbac.vnpt-invoice.com.vn \n')
                                    else:
                                        #driver.get(link_text)
                                        # có thể tải file hoặc không tải được file vì web chưa training
                                        #time.sleep(8)
                                        self.Write_Log(link_output,name_file_log_err, '[WARNING] Kiểm tra link download : ' + str(check_link_text))
                                        self.Write_Log(link_output,name_file_log_err, '[WARNING] Web hiện tại robot chưa được học : \n')
                                        self.Write_Log(link_output,name_file_log_err, '[WARNING] Tiêu đề email : '+ title_email.upper())
                                        self.Write_Log(link_output,name_file_log_err, '==========================================================================')
                                        #driver.back()
                                        time.sleep(3)
                                    time.sleep(3)
                                    # if (check_link_text != 7):
                                    #     check_next_page = 1
                    else:
                        self.Write_Log(link_output,name_file_log_err,"Email Không đúng định dạng tiêu đề \n")
                        self.Write_Log(link_output,name_file_log_err,title_email)
                        self.Write_Log(link_output,name_file_log_err, '==========================================================================')
                        
                    if (idx_email_select_in_page == len(self.arr_id_tr_span) - 1):
                        idx_email_select_in_page = 0
                    else:
                        idx_email_select_in_page += 1
                        
                    print('idx_email_select_in_page',idx_email_select_in_page)
                    time.sleep(3)
                    driver.back()
                    # if check_next_page == 1:
                    #     for item in range(0,current_page):
                    #         print('loop',item)
                    #         self.click_next_page(driver,link_output,name_file_log_err)
                    time.sleep(5)
                    self.get_id_tr_span_arr(driver)
                    
