from Booking_Page import Booking_Page

class Instructor(Booking_Page):
    def __init__(self,name,age,phoneNumber,email,startingDateAndTime,type,specialization2):
        Booking_Page.__init__(self,name,age,phoneNumber,email,startingDateAndTime,type)
        self.__specialization2 = specialization2

    def get_specialization2(self):
        return self.__specialization2

    def set_specialization2(self,specialization2):
        self.__specialization2 = specialization2

instructor = Instructor("Peishan",17,62353535,"171846z@gmail.com","2017-12-11  23:59:59","Doctor","Internal Medicine")
# print(instructor.get_name())
# print(instructor.get_age())
# print(instructor.get_phoneNumber())
# print(instructor.get_email())
# print(instructor.get_startingDateAndTime())
# print(instructor.get_type())
# print(instructor.get_specialization2())