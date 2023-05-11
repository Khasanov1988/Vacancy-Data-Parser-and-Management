import json
from get_data_classes import *
from src.json_saver import JSONSaver


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


def sort_vacancies_from(vacancies: list) -> list:
    """Возвращает отсортированный список вакансий по убыванию минимальной зарплаты"""
    for vacancy in vacancies:
        if vacancy['salary_from'] is None:
            vacancy['salary_from'] = 0
    answer = sorted(vacancies, key=lambda d: d['salary_from'], reverse=True)
    for vacancy in vacancies:
        if vacancy['salary_from'] == 0:
            vacancy['salary_from'] = None
    return answer


def sort_vacancies_to(vacancies: list) -> list:
    """Возвращает отсортированный список вакансий по убыванию минимальной зарплаты"""
    for vacancy in vacancies:
        if vacancy['salary_to'] is None:
            vacancy['salary_to'] = 0
    answer = sorted(vacancies, key=lambda d: d['salary_to'], reverse=True)
    for vacancy in vacancies:
        if vacancy['salary_to'] == 0:
            vacancy['salary_to'] = None
    return answer


def get_top_vacancies(vacancies: list, top_n) -> list:
    """Возвращает N верхних значений списка вакансий"""
    top_n = int(top_n)
    if len(vacancies) > top_n:
        return vacancies[0:top_n]
    else:
        return vacancies


def filter_vacancies(vacancies: list, filter_words) -> list:
    """Возвращает отфильтрованные вакансии по ключевому слову"""
    filtered_vacancies = []
    for vacancy in vacancies:
        flag = False
        val = vacancy.values()
        for items in val:
            words = str(items).split()
            for item in words:
                if item in filter_words.split():
                    filtered_vacancies.append(vacancy)
                    flag = True
                    break
            if flag:
                break

    return filtered_vacancies


def get_vacancies_by_salary(self, salary_min: int, salary_max: int):
    """Возвращает вакансии в диапазоне зарплат"""
    answer = []
    for vacancy in self:
        if isinstance(vacancy["salary_from"], int) and salary_min <= vacancy["salary_from"] <= salary_max:
            answer.append(vacancy)
        elif isinstance(vacancy["salary_to"], int) and salary_min <= vacancy["salary_to"] <= salary_max:
            answer.append(vacancy)
    return answer


def vacancies_parcer():
    """Парсинг вакансий с ресурсов HeadHunter и SuperJob"""
    # Работа источниками
    sources = None
    while sources not in ("1", "2", "3"):
        if sources in ("exit", "выход"):
            exit()
        elif sources is not None:
            print('Вы ввели недопустимую команду. Попробуйте снова или введите "exit" для выхода')
        sources = input(
            "Введите требуемые источники вакансий: 1 - HeadHunter+SuperJob, 2 - HeadHunter, 3 - SuperJob ---> ").lower()
    if sources == "1":
        hh = HeadHunterAPI()
        sj = SuperJobAPI()
    elif sources == "2":
        hh = HeadHunterAPI()
        sj = None
    else:
        hh = None
        sj = SuperJobAPI()
    # Работа с ключевым словом
    keyword: str = input('Введите требуемое ключевое слово для поиска вакансий ---> ')
    # Работа с количеством страниц парсинга
    page_count = None
    while page_count not in (range(1, 51)):
        if page_count in ("exit", "выход"):
            exit()
        elif page_count is not None:
            print('Вы ввели недопустимое значение количества страниц. Попробуйте снова или введите "exit" для выхода')
        page_count = input(
            "Введите требуемое количество страниц вывода от 1 до 50 (на каждой странице по 100 вакансий) ---> ")
        if page_count.isdecimal():
            page_count = int(page_count)
    # Парсинг
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
    # Сохранение данных в файл
    data = JSONSaver(vacancies_hh + vacancies_sj)
    data.save_to_json()
    return data
