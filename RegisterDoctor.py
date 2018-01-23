from Register import Register

class RegisterDoctor(Register):
    def __init__(self, accountType, firstName, lastName, username, password, age, gender, email, contactNumber, specialization1):
        Register.__init__(self,accountType,firstName,lastName,username,password,age,gender,email,contactNumber)
        self.__specialization1 = specialization1

    def get_specialization1(self):
        return self.__specialization1

    def set_specialization1(self,specialization1):
        self.__specialization1 = specialization1

# Doctor = RegisterDoctor("Doctor","Grizz","Bear","weBearBears","123456",1,"Male","grizz@hotmail.com","62353535","Dentist")
# print(Doctor.get_firstName())
# print(instructor.get_name())
# print(instructor.get_age())
# print(instructor.get_phoneNumber())
# print(instructor.get_email())
# print(instructor.get_startingDateAndTime())
# print(instructor.get_type())
# print(instructor.get_specialization2())