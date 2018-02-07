class Login:
    def __init__(self,accountType,username,password, firstName, lastName):
        self.__registerid=""
        self.__accountType = accountType
        self.__username = username
        self.__password = password
        self.__firstName = firstName
        self.__lastName = lastName


    def get_accountType(self):
        return self.__accountType
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_registerid(self):
        return self.__registerid
    def get_firstName(self):
        return self.__firstName
    def get_lastName(self):
        return self.__lastName


    def set_registerid(self,registerid):
        self.__registerid = registerid