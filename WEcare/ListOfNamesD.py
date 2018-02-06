class ListOfNamesD():
    def __init__(self,accountType,firstName,lastName,username,specialization):
        self.__accountType = accountType
        self.__firstName = firstName
        self.__lastName = lastName
        self.__username = username
        self.__specialization = specialization

    def get_accountType(self):
        return self.__accountType
    def get_firstName(self):
        return self.__firstName
    def get_lastName(self):
        return self.__lastName
    def get_username(self):
        return self.__username
    def get_specialization(self):
        return self.__specialization

    def set_account(self,accountType):
        self.__accountType = accountType
    def set_firstName(self,firstName):
        self.__firstName = firstName
    def set_lastName(self,lastName):
        self.__lastName = lastName
    def set_username(self,username):
        self.__username = username
    def set_specialization1(self,specialization):
        self.__specialization1 = specialization