from get_data_classes import *
from src.json_saver import JSONSaver


def printj(dict_to_print: dict) -> None:
    """Prints a dictionary in a JSON-like format with indentation"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


def sort_vacancies_from(vacancies: list) -> list:
    """Returns a sorted list of vacancies in descending order of minimum salary"""
    for vacancy in vacancies:
        if vacancy['salary_from'] is None:
            vacancy['salary_from'] = 0
    answer = sorted(vacancies, key=lambda d: d['salary_from'], reverse=True)
    for vacancy in vacancies:
        if vacancy['salary_from'] == 0:
            vacancy['salary_from'] = None
    return answer


def sort_vacancies_to(vacancies: list) -> list:
    """Returns a sorted list of vacancies in descending order of maximum salary"""
    for vacancy in vacancies:
        if vacancy['salary_to'] is None:
            vacancy['salary_to'] = 0
    answer = sorted(vacancies, key=lambda d: d['salary_to'], reverse=True)
    for vacancy in vacancies:
        if vacancy['salary_to'] == 0:
            vacancy['salary_to'] = None
    return answer


def get_top_vacancies(vacancies: list, top_n) -> list:
    """Returns the top N values from the list of vacancies"""
    top_n = int(top_n)
    if len(vacancies) > top_n:
        return vacancies[0:top_n]
    else:
        return vacancies


def filter_vacancies(vacancies: list, filter_words) -> list:
    """Returns filtered vacancies based on a keyword"""
    filtered_vacancies = []
    for vacancy in vacancies:
        flag = False
        val = vacancy.values()
        for items in val:
            words = str(items).split()
            for item in words:
                if item.lower() in filter_words.split():
                    filtered_vacancies.append(vacancy)
                    flag = True
                    break
            if flag:
                break
    return filtered_vacancies


def get_vacancies_by_salary(self, salary_min: int, salary_max: int):
    """Returns vacancies within a salary range"""
    answer = []
    for vacancy in self:
        if isinstance(vacancy["salary_from"], int) and salary_min <= vacancy["salary_from"] <= salary_max:
            answer.append(vacancy)
        elif isinstance(vacancy["salary_to"], int) and salary_min <= vacancy["salary_to"] <= salary_max:
            answer.append(vacancy)
    return answer


def vacancies_parser():
    """Parsing vacancies from HeadHunter and SuperJob resources"""
    # Selecting data sources
    sources = None
    while sources not in ("1", "2", "3"):
        if sources in ("exit", "выход"):
            exit()
        elif sources is not None:
            print('You entered an invalid command. Please try again or enter "exit" to exit')
        sources = input(
            "Enter the desired sources of vacancies: 1 - HeadHunter+SuperJob, 2 - HeadHunter, 3 - SuperJob ---> ").lower()
    if sources == "1":
        hh = HeadHunterAPI()
        sj = SuperJobAPI()
    elif sources == "2":
        hh = HeadHunterAPI()
        sj = None
    else:
        hh = None
        sj = SuperJobAPI()
    # Working with keywords
    keyword: str = input('Enter the desired keyword for vacancy search ---> ')
    # Working with the number of parsing pages
    page_count = None
    while page_count not in (range(1, 51)):
        if page_count in ("exit", "выход"):
            exit()
        elif page_count is not None:
            print('You entered an invalid number of pages. Please try again or enter "exit" to exit')
        page_count = input(
            "Enter the desired number of output pages from 1 to 50 (each page contains 100 vacancies) ---> ")
        if page_count.isdecimal():
            page_count = int(page_count)
    # Parsing
    if hh is not None:
        hh.get_vacancies(keyword, int(page_count))
        vacancies_hh = hh.get_corrected_vacancies()
    else:
        vacancies_hh = []

    if sj is not None:
        sj.get_vacancies(keyword, int(page_count))
        vacancies_sj = sj.get_corrected_vacancies()
    else:
        vacancies_sj = []
    # Saving data to a file
    data = JSONSaver(vacancies_hh + vacancies_sj)
    data.save_to_json()
    return data
