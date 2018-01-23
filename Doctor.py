from BookingPage import BookingPage


class Doctor(BookingPage):
    def __init__(self, name, age, phoneNumber, email, startingDateAndTime,type, created_by,specialization1):
        BookingPage.__init__(self,name, age, phoneNumber, email, startingDateAndTime,type, created_by)
        self.__specialization1 = specialization1

    def get_specialization1(self):
        return self.__specialization1

    def set_specialization(self, specialization1):
        self.__specialization1 = specialization1