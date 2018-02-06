class BookingPage():
    def __init__(self,name,age,phoneNumber,email,startingDateAndTime,type,created_by):
        self.__typeid = ""
        self.__name = name
        self.__age = age
        self.__phoneNumber = phoneNumber
        self.__email = email
        self.__startingDateAndTime = startingDateAndTime
        self.__type = type
        self.__created_by =  created_by

    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_phoneNumber(self):
        return self.__phoneNumber
    def get_email(self):
        return self.__email
    def get_startingDateAndTime(self):
        return self.__startingDateAndTime
    def get_type(self):
        return self.__type


    def set_name(self,name):
        self.__name = name
    def set_age(self,age):
        self.__age = age
    def set_phoneNumber(self,phoneNumber):
        self.__phoneNumber = phoneNumber
    def set_email(self,email):
        self.__email = email
    def set_startingDateAndTime(self,startingDateAndTime):
        self.__startingDateAndTime = startingDateAndTime
    def set_type(self,type):
        self.__type = type

    def get_typeid(self):
        return self.__typeid

    def set_typeid(self,typeid):
        self.__typeid = typeid

    def get_created_by(self):
        return self.__created_by

    def set_created_by(self,created_by):
        self.__created_by = created_by