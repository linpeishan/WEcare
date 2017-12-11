import Booking_Page as bp

class Instructor():
    def __init__(self,name,age,phoneNumber,email,dateAndTime,specialization):
        bp.bookingPage.__init__(type,name,age,phoneNumber,email,dateAndTime)
        self.__specialization = specialization

    def get_specialization(self):
        return self.__specialization

    def set_specialization(self,specialization):
        self.__specialization = specialization

