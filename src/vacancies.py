class ComparisonError(Exception):
    def __str__(self):
        return "Ошибка в сравнении. В каком-то из вакансий может быть не указана зарплата"


class Vacancy:
    __slots__ = ['source', 'id', 'title', 'employer', 'link', 'area', 'salary_from', 'salary_to', 'salary_currency']

    def __init__(self, enter_dict: dict):
        self.source = enter_dict['source']
        self.id = enter_dict['id']
        self.title = enter_dict['title']
        self.employer = enter_dict['client']
        self.link = enter_dict['link']
        self.area = enter_dict['area']
        self.salary_from = enter_dict['salary_from']
        self.salary_to = enter_dict['salary_to']
        self.salary_currency = enter_dict['salary_currency']

    def __lt__(self, other):
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from < other.__salary_from:
                return True
            else:
                return False

    def __le__(self, other):
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from <= other.__salary_from:
                return True
            else:
                return False

    def __gt__(self, other):
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from > other.__salary_from:
                return True
            else:
                return False

    def __ge__(self, other):
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from >= other.__salary_from:
                return True
            else:
                return False
