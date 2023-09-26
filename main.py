from src.utils import *
from src.json_saver import *


def main():
    # Check if it is necessary to parse data again or if it is sufficient to take data from the file
    is_parser_needed = input(
        'Do you need to read data from the "data.json" file?\n'
        '"Yes" - read data from the file\n'
        'any other input - parse data again\n')
    if is_parser_needed.lower() in ("yes", "y"):
        try:
            # Load data from the file
            file = open('data.json', 'r', encoding='utf-8')
            vacancies_all = json.load(file)
            data = JSONSaver(vacancies_all)
            file.close()
        except Exception:
            print("The file is not supported. Please try again.")
            exit()
    else:
        # Parse data from websites
        data = vacancies_parser()
        vacancies_all = data.data
    # Loop for handling user commands
    while True:
        # Display the user menu
        print(f'\n\nCurrently, there are {len(vacancies_all)} vacancies in the list')
        print('Enter the desired command:\n'
              '1 - Sort vacancies by decreasing minimum salary\n'
              '2 - Sort vacancies by decreasing maximum salary\n'
              '3 - Filter the top N vacancies from the list\n'
              '4 - Filter vacancies by keyword\n'
              '5 - Filter vacancies by salary range\n'
              '6 - Return to the original list of vacancies\n'
              '7 - Delete a vacancy from the shared file by id\n'
              '8 - Add a vacancy to the shared file\n'
              '"print" - Print vacancies to the console\n'
              '"exit" - Exit\n'
              'COMMAND: ')
        command = input().lower()
        # Check user input and execute corresponding functions
        if command == "1":
            vacancies_all = sort_vacancies_from(vacancies_all)
        elif command == "2":
            vacancies_all = sort_vacancies_to(vacancies_all)
        elif command == "3":
            top_n = input('Enter the number of top vacancies to keep ---> ')
            if top_n.isdecimal():
                vacancies_all = get_top_vacancies(vacancies_all, top_n)
            else:
                print('You entered an invalid value')
        elif command == "4":
            filter_words = input('Enter the keyword to filter vacancies ---> ').lower()
            vacancies_all = filter_vacancies(vacancies_all, filter_words)
        elif command == "5":
            salaries = input('Enter the minimum and maximum salary values separated by a space ---> ').strip()
            if len(salaries.split()) == 2:
                if salaries.split()[0].isdecimal():
                    salary_min = int(salaries.split()[0])
                else:
                    print('You entered an invalid value, please try the command again')
                    salary_min = None
                if salaries.split()[1].isdecimal():
                    salary_max = int(salaries.split()[0])
                else:
                    print('You entered an invalid value, please try the command again')
                    salary_max = None
                if salary_max is not None and salary_min is not None:
                    vacancies_all = get_vacancies_by_salary(vacancies_all, salary_min, salary_max)
            else:
                print('Incorrect input')
        elif command == "6":
            vacancies_all = data.data
        elif command == "7":
            vacancy_id = input('Enter the id of the vacancy you want to delete ---> ')
            if vacancy_id.isdecimal():
                vacancy_id = int(vacancy_id)
                data.delete_vacancy(vacancy_id)
                vacancies_all = data.data
            else:
                print('You entered an invalid value')
        elif command == "8":
            vac = {"source": "UserAddedVacancy",
                   "id": input('Enter the vacancy id ---> '),
                   "title": input('Enter the vacancy title ---> '),
                   "client": input('Enter the employer name ---> '),
                   "link": input('Enter the vacancy link ---> '),
                   "area": input('Enter the city of the vacancy ---> '),
                   "salary_from": input('Enter the "FROM" salary ---> '),
                   "salary_to": input('Enter the "TO" salary ---> '),
                   "salary_currency": input('Enter the currency symbol for salary ---> ')}
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
            print('You entered an invalid command. Please try again or enter "exit" to exit')


if __name__ == '__main__':
    main()
