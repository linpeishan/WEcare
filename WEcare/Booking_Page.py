# Booking Page

#TYPE: DOCTOR/ INSTRUCTOR
#SPECIALIZATION
#======================
#Name
#Age
#phoneNumber
#Email
#Date and Time

import datetime

class bookingPage():
    def __init__(self,name,age,phoneNumber,email,dateAndTime):
        self.__name = name
        self.__age = age
        self.__phoneNumber = phoneNumber
        self.__email = email
        self.__dateAndTime = dateAndTime

    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_phoneNumber(self):
        return self.__phoneNumber
    def get_email(self):
        return self.__email
    def get_dateAndTime(self):
        return self.__dateAndTime

    def set_name(self,name):
        self.__name = name
    def set_age(self,age):
        self.__age = age
    def set_phoneNumber(self,phoneNumber):
        self.__phoneNumber = phoneNumber
    def set_email(self,email):
        self.__email = email
    def set_dateAndTime(self,dateAndTime):
        self.__dateAndTime = dateAndTime
