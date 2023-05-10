from utils import *


def main():
    is_parcer_needed = input(
        'Введите нужно ли считать данные с файла "data.json". В противном случае данные будут спарсены по новой\n'
        '"Yes" - нужно считать данные из файла\n'
        'любой другой ввод - прочитать данные из файла\n')
    if is_parcer_needed in ("Yes", "Y"):
        try:
            file = open('data.json', 'r', encoding='utf-8')
            vacancies_all = json.load(file)
        except Exception:
            print("Файл не поддерживается. Попробуйте сначала")
            file.close()
            exit()
        finally:
            file.close()
    else:
        data = vacancies_parcer()
        vacancies_all = data.data



    vacancies = vacancies_all

    while True:
        print(f'\n\nНа текущий момент в списке {len(vacancies)} вакансий')
        print('Введите требуемую команду:\n'
              '1 - Отсортировать вакансии по убыванию минимальной зарплаты\n'
              '2 - Отсортировать вакансии по убыванию максимальной зарплаты\n'
              '3 - Оставить N верхних вакансий списка\n'
              '4 - Найти вакансию по ключевому слову\n'
              '5 - Отсортировать вакансии в диапазоне зарплат\n'
              '6 - Вернуться к первоначальному списку вакансий\n'
              '"print" - Вывести вакансии в консоль\n'
              '"exit" - выход\n'
              'КОМАНДА: ')
        command = input().lower()
        if command == "1":
            vacancies = sort_vacancies_from(vacancies)
        elif command == "2":
            vacancies = sort_vacancies_to(vacancies)
        elif command == "3":
            top_n = input('Введите количество верхних вакансий списка, которые нужно оставить ---> ')
            if top_n.isdecimal():
                vacancies = get_top_vacancies(vacancies, top_n)
            else:
                print('Вы ввели недопустимое значение')
        elif command == "4":
            filter_words = input('Введите ключевое слово по которому нужно отфильтровать вакансии ---> ')
            vacancies = filter_vacancies(vacancies, filter_words)
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
            vacancies = get_vacancies_by_salary(vacancies, salary_min, salary_max)
        elif command == "6":
            vacancies = vacancies_all
        elif command == "print":
            printj(vacancies)
        elif command == "exit":
            exit()
        else:
            print('Вы ввели недопустимую команду. Попробуйте снова или введите "exit" для выхода')


if __name__ == '__main__':
    main()
