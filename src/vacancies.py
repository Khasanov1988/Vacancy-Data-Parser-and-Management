class ComparisonError(Exception):



class Vacancy:
    __slots__ = ['__source', '__id', '__title', '__employer', '__link', '__area', '__salary_from', '__salary_to',
                 '__salary_currency']

    def __init__(self, enter_dict: dict):
        self.__source = enter_dict['source']
        self.__id = enter_dict['id']
        self.__title = enter_dict['title']
        self.__employer = enter_dict['client']
        self.__link = enter_dict['link']
        self.__area = enter_dict['area']
        self.__salary_from = enter_dict['salary_from']
        self.__salary_to = enter_dict['salary_to']
        self.__salary_currency = enter_dict['salary_currency']


    def __lt__(self, other):
        if self.__salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.__salary_from < other.__salary_from
                return True
            else:
                return False

    def __le__(self, other):
        if self.__salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.__salary_from <= other.__salary_from
                return True
            else:
                return False

    def __gt__(self, other):
        if self.__salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.__salary_from > other.__salary_from
                return True
            else:
                return False

    def __ge__(self, other):
        if self.__salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.__salary_from >= other.__salary_from
                return True
            else:
                return False
