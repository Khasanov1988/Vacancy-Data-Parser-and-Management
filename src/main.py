from utils import *
from json_saver import *


def main():
    # Проверяем нужно ли парсить данные по новой или достаточно взять данные из файла
    is_parcer_needed = input(
        'Нужно ли считать данные из файла "data.json"?\n'
        '"Yes" - нужно считать данные из файла\n'
        'любой другой ввод - спарсить данные по новой\n')
    if is_parcer_needed in ("Yes", "Y"):
        try:
            # Загружаем данные из файла
            file = open('data.json', 'r', encoding='utf-8')
            vacancies_all = json.load(file)
            data = JSONSaver(vacancies_all)
        except Exception:
            print("Файл не поддерживается. Попробуйте сначала")
            file.close()
            exit()
        finally:
            file.close()
    else:
        # Парсим данные с сайтов
        data = vacancies_parcer()
        vacancies_all = data.data
    # Цикл работы с пользовательскими командами
    while True:
        # Вывод пользовательского меню
        print(f'\n\nНа текущий момент в списке {len(vacancies_all)} вакансий')
        print('Введите требуемую команду:\n'
              '1 - Отсортировать вакансии по убыванию минимальной зарплаты\n'
              '2 - Отсортировать вакансии по убыванию максимальной зарплаты\n'
              '3 - Отфильтровать N верхних вакансий списка\n'
              '4 - Отфильтровать вакансию по ключевому слову\n'
              '5 - Отфильтровать вакансии в диапазоне зарплат\n'
              '6 - Вернуться к исходному списку вакансий\n'
              '7 - Удалить вакансию из общего файла по id\n'
              '8 - Добавить вакансию в общий файл\n'
              '"print" - Вывести вакансии в консоль\n'
              '"exit" - выход\n'
              'КОМАНДА: ')
        command = input().lower()
        # Проверка пользовательского ввода и запуск соответствующих функций
        if command == "1":
            vacancies_all = sort_vacancies_from(vacancies_all)
        elif command == "2":
            vacancies_all = sort_vacancies_to(vacancies_all)
        elif command == "3":
            top_n = input('Введите количество верхних вакансий списка, которые нужно оставить ---> ')
            if top_n.isdecimal():
                vacancies_all = get_top_vacancies(vacancies_all, top_n)
            else:
                print('Вы ввели недопустимое значение')
        elif command == "4":
            filter_words = input('Введите ключевое слово по которому нужно отфильтровать вакансии ---> ').lower()
            vacancies_all = filter_vacancies(vacancies_all, filter_words)
        elif command == "5":
            salaries = input('Введите минимальное и максимальное значение зарплат через пробел ---> ').strip()
            if salaries.split()[0].isdecimal():
                salary_min = int(salaries.split()[0])
            else:
                print('Вы ввели недопустимое значение, повторите команду по новой')
                salary_min = None
            if salaries.split()[1].isdecimal():
                salary_max = int(salaries.split()[0])
            else:
                print('Вы ввели недопустимое значение, повторите команду по новой')
                salary_max = None
            if salary_max is not None and salary_min is not None:
                vacancies_all = get_vacancies_by_salary(vacancies_all, salary_min, salary_max)
        elif command == "6":
            vacancies_all = data.data
        elif command == "7":
            vacancy_id = input('Введите id вакансии, которую хотите удалить ---> ')
            if vacancy_id.isdecimal():
                vacancy_id = int(vacancy_id)
                data.delete_vacancy(vacancy_id)
                vacancies_all = data.data
            else:
                print('Вы ввели недопустимое значение')
        elif command == "8":
            vac = {"source": "UserAddedVacancy",
                   "id": input('Введите id вакансии ---> '),
                   "title": input('Введите название вакансии ---> '),
                   "client": input('Введите название работодателя ---> '),
                   "link": input('Введите ссылку на вакансию ---> '),
                   "area": input('Введите город вакансии ---> '),
                   "salary_from": input('Введите зарплату "ОТ" ---> '),
                   "salary_to": input('Введите зарплату "ДО" ---> '),
                   "salary_currency": input('Введите обозначение валюты зарплаты ---> ')}
            try:
                vac["id"] = int(vac["id"])
                vac["salary_from"] = int(vac["salary_from"])
                vac["salary_to"] = int(vac["salary_to"])
            except ValueError:
                vac["id"] = vac["salary_from"] = vac["salary_to"] = None
            vacancy = Vacancy(vac)
            data.add_vacancy(vacancy)
            vacancies_all = data.data
        elif command == "print":
            printj(vacancies_all)
        elif command == "exit":
            exit()
        else:
            print('Вы ввели недопустимую команду. Попробуйте снова или введите "exit" для выхода')


if __name__ == '__main__':
    main()
