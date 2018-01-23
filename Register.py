class Register():
    def __init__(self,accountType,firstName,lastName,username,password,age,gender,email,contactNumber):
        self.__registerid=""
        self.__accountType = accountType
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__password = password
        self.__age = age
        self.__gender = gender
        self.__email = email
        self.__contactNumber = contactNumber

    def get_accountType(self):
        return self.__accountType
    def get_firstName(self):
        return self.__firstName
    def get_lastName(self):
        return self.__lastName
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_age(self):
        return self.__age
    def get_gender(self):
        return self.__gender
    def get_email(self):
        return self.__email
    def get_contactNumber(self):
        return self.__contactNumber
    def get_registerid(self):
        return self.__registerid

    def set_account(self,accountType):
        self.__accountType = accountType
    def set_firstName(self,firstName):
        self.__firstName = firstName
    def set_lastName(self,lastName):
        self.__lastName = lastName
    def set_username(self,username):
        self.__username = username
    def set_password(self,password):
        self.__password = password
    def set_age(self,age):
        self.__age = age
    def set_gender(self,gender):
        self.__gender = gender
    def set_email(self,email):
        self.__email = email
    def set_contactNumber(self,contactNumber):
        self.__contactNumber = contactNumber
    def set_registerid(self,registerid):
        self.__registerid = registerid

User = Register("User","Grizz","Bear","weBearBears","123456",1,"Male","grizz@hotmail.com","62353535")