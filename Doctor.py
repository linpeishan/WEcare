from Booking_Page import Booking_Page


class Doctor(Booking_Page):
    def __init__(self, name, age, phoneNumber, email, startingDateAndTime,type, specialization1):
        Booking_Page.__init__(self,name, age, phoneNumber, email, startingDateAndTime,type)
        self.__specialization1 = specialization1

    def get_specialization1(self):
        return self.__specialization1

    def set_specialization(self, specialization1):
        self.__specialization1 = specialization1

# doctor = Doctor("Peishan",17,62353535,"171846z@gmail.com","2017-12-11  23:59:59","Doctor","Internal Medicine")
# print(doctor.get_name())
# print(doctor.get_age())
# print(doctor.get_phoneNumber())
# print(doctor.get_email())
# print(doctor.get_startingDateAndTime())
# print(doctor.get_type())
# print(doctor.get_specialization1())