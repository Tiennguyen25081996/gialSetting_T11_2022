#import logic
import time
from Logic.EInvoiceDownLoad_logic import EInvoiceDownloadLogic
import threading
#pip install pyDrive
#pip install --upgrade google-api-python-client
#pip install openpyxl

if __name__ == '__main__':
    ojb_EInvoiceDownloadLogic = EInvoiceDownloadLogic()
    arr_active_company = ojb_EInvoiceDownloadLogic.start_EInvoice()
    threads = []
    for company_id in arr_active_company:
        print('company_id',company_id)
        processThread = threading.Thread(target=ojb_EInvoiceDownloadLogic.Company, args=(company_id,))
        threads.append(processThread)
        processThread.start()
        time.sleep(2)
        
    
    for item in threads:
        item.join()
    