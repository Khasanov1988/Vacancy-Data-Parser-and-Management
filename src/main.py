from get_data_classes import *
from src.json_saver import JSONSaver
from src.vacancies import Vacancy


def main():
    keyword = 'Python'
    hh = HeadHunterAPI()
    sj = SuperJobAPI()
    for api in (hh, sj):
        api.get_vacancies(keyword, page_count=1)
    vacancies_json = hh.get_corrected_vacancies() + sj.get_corrected_vacancies()
    data = JSONSaver(vacancies_json)
    data.save_to_json()
    vacancy = Vacancy({
        "source": "Личная",
        "id": 99999,
        "title": "test",
        "client": None,
        "link": None,
        "area": None,
        "salary_from": None,
        "salary_to": None,
        "salary_currency": None
    })
    data.add_vacancy(vacancy)
    data.delete_vacancy(99999)


if __name__ == '__main__':
    main()
