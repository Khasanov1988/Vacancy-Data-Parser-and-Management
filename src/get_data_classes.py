import os
import requests
from abc import ABC, abstractmethod
import json

class ParsingError(Exception):
    def __str__(self):
        return 'Error fetching data from the API.'

class AbcApi(ABC):
    @abstractmethod
    def get_request(self):
        """
        Abstract method for making API requests.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword, page_count):
        """
        Abstract method for retrieving vacancy information.
        """
        pass

    @abstractmethod
    def get_corrected_vacancies(self):
        """
        Abstract method for converting data into the desired format.
        """
        pass

    @staticmethod
    def print_json(dict_to_print: dict) -> None:
        """Prints a dictionary in a JSON-like format with indentation."""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class HeadHunterAPI(AbcApi):
    def __init__(self):
        self.__header = {
            "User-Agent": "unknown"
        }
        self.__params = {
            "text": None,
            "page": 0,
            "per_page": 100
        }
        self.__vacancies = []

    def get_vacancies(self, keyword, page_count=1):
        self.__params["text"] = keyword
        while self.__params['page'] < page_count:
            print(f"HeadHunter, Parsing page {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Error fetching data!')
                break
            print(f"Found ({len(values)}) vacancies.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_corrected_vacancies(self):
        corrected_vacancies = []
        for item in self.__vacancies:
            corrected_vacancies.append({
                "source": "HeadHunter",
                "id": int(item["id"]),
                "title": item["name"],
                "client": item["employer"]["name"],
                "link": item["alternate_url"],
                "area": item["area"]["name"]
            })
            if item["salary"] is not None:
                corrected_vacancies[-1]["salary_from"] = item["salary"]["from"]
                corrected_vacancies[-1]["salary_to"] = item["salary"]["to"]
                corrected_vacancies[-1]["salary_currency"] = item["salary"]["currency"]
            else:
                corrected_vacancies[-1]["salary_from"] = corrected_vacancies[-1]["salary_to"] = corrected_vacancies[-1][
                    "salary_currency"] = None
        return corrected_vacancies

    @property
    def vacancies(self):
        return self.__vacancies

class SuperJobAPI(AbcApi):
    def __init__(self):
        self.__header = {'X-Api-App-Id': os.getenv('SUPER_JOB_API_KEY')}
        self.__params = {
            "keyword": None,
            "page": 0,
            "count": 100
        }
        self.__vacancies = []

    def get_vacancies(self, keyword, page_count=1):
        self.__params["keyword"] = keyword
        while self.__params['page'] < page_count:
            print(f"SuperJob, Parsing page {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Error fetching data!')
                break
            print(f"Found ({len(values)}) vacancies.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_request(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['objects']

    def get_corrected_vacancies(self):
        corrected_vacancies = []
        for item in self.__vacancies:
            corrected_vacancies.append({
                "source": "SuperJob",
                "id": item["id"],
                "title": item["profession"],
                "client": item["firm_name"],
                "link": item["link"],
                "area": item["town"]["title"],
                "salary_from": item["payment_from"],
                "salary_to": item["payment_to"],
                "salary_currency": item["currency"]
            })
            if corrected_vacancies[-1]["salary_from"] == 0:
                corrected_vacancies[-1]["salary_from"] = None
            if corrected_vacancies[-1]["salary_to"] == 0:
                corrected_vacancies[-1]["salary_to"] = None
        return corrected_vacancies
