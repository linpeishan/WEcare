import Booking_Page as bp


class Doctor():
    def __init__(self, name, age, phoneNumber, email, dateAndTime, specialization):
        bp.bookingPage.__init__(name, age, phoneNumber, email, dateAndTime)
        self.__specialization = specialization

    def get_specialization(self):
        return self.__specialization

    def set_specialization(self, specialization):
        self.__specialization = specialization