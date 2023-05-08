from get_data_classes import *


def main():
    vacancies_json = []
    keyword = 'Python'
    hh = HeadHunterAPI()
    sj = SuperJobAPI()
    for api in (hh, sj):
        api.get_vacancies(keyword, page_count=1)
    vacancies_json.extend(hh.get_corrected_vacancies())
    vacancies_json.extend(sj.get_corrected_vacancies())
    hh.printj(vacancies_json)


if __name__ == '__main__':
    main()
