import os
import requests
from abc import ABC, abstractmethod
import json


class ParsingError(Exception):
    def __str__(self):
        return 'Ошибка получения данных по API.'


class AbcApi(ABC):

    @abstractmethod
    def get_request(self):
        """
        Класс для подключения к API сервиса
        :return:
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword, page_count):
        """
        Класс для получения информации по вакансиям
        :return:
        """
        pass

    @abstractmethod
    def get_corrected_vacancies(self):
        """
        Класс для конвертирования информации в надлежащий вид
        :return:
        """
        pass

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
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
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий.")
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
                "id": item["id"],
                "title": item["name"],
                "client": item["employer"]["name"],
                "link": item["url"],
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
            print(f"SuperJob, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий.")
            self.__vacancies.extend(values)
            print(type(self.__vacancies))
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
