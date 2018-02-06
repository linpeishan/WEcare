class Reviews:
    def __init__(self, message):
        self.__typeid = ""
        self.__message = message

    def get_message(self):
        return self.__message

    def get_typeid(self):
        return self.__typeid

    def set_typeid(self, typeid):
        self.__typeid = typeid
