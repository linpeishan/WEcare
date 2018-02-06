from BookingPage import BookingPage

class Instructor(BookingPage):
    def __init__(self,name,age,phoneNumber,email,startingDateAndTime,type,created_by,specialization2):
        BookingPage.__init__(self,name,age,phoneNumber,email,startingDateAndTime,type,created_by)
        self.__specialization2 = specialization2

    def get_specialization2(self):
        return self.__specialization2

    def set_specialization2(self,specialization2):
        self.__specialization2 = specialization2