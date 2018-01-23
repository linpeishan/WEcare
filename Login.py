class Login:
    def __init__(self,accountType,username,password):
        self.__registerid=""
        self.__accountType = accountType
        self.__username = username
        self.__password = password


    def get_accountType(self):
        return self.__accountType
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_registerid(self):
        return self.__registerid

    def set_account(self,accountType):
        self.__accountType = accountType
    def set_username(self,username):
        self.__username = username
    def set_password(self,password):
        self.__password = password

    def set_registerid(self,registerid):
        self.__registerid = registerid