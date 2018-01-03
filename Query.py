class QueryPage():
    def _init__(self, query):
        self._query = query

    def get_query(self):
        return self._query

    def set_query(self, query):
        self._query= query