from Register import Register

class RegisterInstructor(Register):
    def __init__(self, accountType, firstName, lastName, username, password, age, gender, email, contactNumber, specialization2):
        Register.__init__(self,accountType,firstName, lastName, username, password, age, gender, email, contactNumber)

        self.__specialization2 = specialization2


    def get_specialization2(self):
        return self.__specialization2



    def set_specialization2(self, specialization2):
        self.__specialization2 = specialization2

Instructor = RegisterInstructor("Doctor","Grizz","Bear","weBearBears","123456",1,"Male","grizz@hotmail.com","62353535","Dentist")