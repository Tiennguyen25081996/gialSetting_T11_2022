class SheetWeb:
    ID = None
    Link = None
    UserName = None
    Passwork = None
    Active = None
    TaxCode = None
        
    def set_ID(self,id):
        self.ID = id
        
    def get_ID(self):
        return self.ID
    
    def set_Link(self,link):
        self.Link = link
        
    def get_Link(self):
        return self.Link
    
    def set_Username(self,username):
        self.UserName = username
        
    def get_Username(self):
        return self.UserName
    
    def set_Password(self,password):
        self.Passwork = password
        
    def get_Passwork(self):
        return self.Passwork
    
    def set_Ativce(self,activce):
        self.Active = activce
        
    def get_Active(self):
        return self.Active
    
    def set_TaxCode(self,taxCode):
            self.TaxCode = taxCode
        
    def get_TaxCode(self):
        return self.TaxCode
    