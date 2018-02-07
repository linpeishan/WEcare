class QueryPage():
    def __init__(self, query, date_time, created_by):
        self.__query = query
        self.__date_time = date_time
        self.__created_by = created_by
        self.__enquiryid = ''

    def get_query(self):
        return self.__query

    def get_date_time(self):
        return self.__date_time

    def get_created_by(self):
        return self.__created_by

    def get_enquiryid(self):
        return self.__enquiryid

    def set_query(self, query):
        self.__query= query

    def set_date_time(self, date_time):
        self.__date_time = date_time

    def set_created_by(self, created_by):
        self.__created_by = created_by

    def set_enquiryid(self, enquiryid):
        self.__enquiryid = enquiryid

class FitnessArticle():
    def __init__(self, title, content, type):
        self.__title = title
        self.__content = content
        self.__type = type
        self.__articleid = ''

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_articleid(self):
        return self.__articleid

    def set_articleid(self, articleid):
        self.__articleid = articleid

class DietaryArticle():
    def __init__(self, title, content, type):
        self.__title = title
        self.__content = content
        self.__type = type
        self.__articleid = ''

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_articleid(self):
        return self.__articleid

    def set_articleid(self, articleid):
        self.__articleid = articleid

class EnquiryAnswers:
    def __init__(self, answer, enquiryid, doctorName):
        self.__answer = answer
        self.__enquiryid = enquiryid
        self.__answerid = ''
        self.__doctorName = doctorName

    def get_answer(self):
        return self.__answer

    def get_enquiryid(self):
        return self.__enquiryid

    def get_answerid(self):
        return self.__answerid

    def get_doctorName(self):
        return self.__doctorName

    def set_answer(self, answer):
        self.__answer = answer

    def set_enquiryid(self, enquiryid):
        self.__enquiryid = enquiryid

    def set_answerid(self, answerid):
        self.__answerid = answerid

    def set_doctorName(self, doctorName):
        self.__doctorName = doctorName