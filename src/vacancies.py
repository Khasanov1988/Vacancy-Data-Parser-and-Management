class ComparisonError(Exception):
    """Custom error class for vacancy comparison."""
    def __str__(self):
        return "Error in comparison. Salary may not be specified in one of the vacancies."


class Vacancy:
    """
    Vacancy class
    """
    __slots__ = ['source', 'id', 'title', 'employer', 'link', 'area', 'salary_from', 'salary_to', 'salary_currency']
    all_vacancies = []

    def __init__(self, enter_dict: dict):
        """Initialize the class"""
        self.source = enter_dict['source']
        self.id = enter_dict['id']
        self.title = enter_dict['title']
        self.employer = enter_dict['client']
        self.link = enter_dict['link']
        self.area = enter_dict['area']
        self.salary_from = enter_dict['salary_from']
        self.salary_to = enter_dict['salary_to']
        self.salary_currency = enter_dict['salary_currency']
        self.all_vacancies.append(self)

    def __str__(self):
        """Override the str magic method"""
        return f"Vacancy from {self.source} with id: {self.id}"

    def __repr__(self):
        """Override the repr magic method"""
        return f"Vacancy(source: {self.source}, id: {self.id}, title: {self.title}, " \
               f"employer: {self.employer}, link: {self.link}, area: {self.area}, " \
               f"salary_from: {self.salary_from}, salary_to: {self.salary_to}, " \
               f"salary_currency: {self.salary_currency}"

    def __lt__(self, other):
        """Override the lt magic method"""
        if self.salary_from is None or other.salary_from is None:
            raise ComparisonError
        else:
            return self.salary_from < other.salary_from

    def __le__(self, other):
        """Override the le magic method"""
        if self.salary_from is None or other.salary_from is None:
            raise ComparisonError
        else:
            return self.salary_from <= other.salary_from

    def __gt__(self, other):
        """Override the gt magic method"""
        if self.salary_from is None or other.salary_from is None:
            raise ComparisonError
        else:
            return self.salary_from > other.salary_from

    def __ge__(self, other):
        """Override the ge magic method"""
        if self.salary_from is None or other.salary_from is None:
            raise ComparisonError
        else:
            return self.salary_from >= other.salary_from
