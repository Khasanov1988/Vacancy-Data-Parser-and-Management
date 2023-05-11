from utils import *


def main():
    # Проверяем нужно ли парсить данные по новой или достаточно взять данные из файла
    is_parcer_needed = input(
        'Введите нужно ли считать данные с файла "data.json". В противном случае данные будут спарсены по новой\n'
        '"Yes" - нужно считать данные из файла\n'
        'любой другой ввод - прочитать данные из файла\n')
    if is_parcer_needed in ("Yes", "Y"):
        try:
            # Берем данные из файла
            file = open('data.json', 'r', encoding='utf-8')
            vacancies_all = json.load(file)
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
            filter_words = input('Введите ключевое слово по которому нужно отфильтровать вакансии ---> ')
            vacancies_all = filter_vacancies(vacancies_all, filter_words)
        elif command == "5":
            salaries = input('Введите минимальное и максимальное значение зарплат через пробел ---> ').strip()
            if salaries.split()[0].isdecimal():
                salary_min = int(salaries.split()[0])
            else:
                print('Вы ввели недопустимое значение')
            if salaries.split()[1].isdecimal():
                salary_max = int(salaries.split()[0])
            else:
                print('Вы ввели недопустимое значение')
            vacancies_all = get_vacancies_by_salary(vacancies_all, salary_min, salary_max)
        elif command == "6":
            vacancies_all = vacancies_all
        elif command == "print":
            printj(vacancies_all)
        elif command == "exit":
            exit()
        else:
            print('Вы ввели недопустимую команду. Попробуйте снова или введите "exit" для выхода')


if __name__ == '__main__':
    main()
