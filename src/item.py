from abc import ABC, abstractmethod
import requests
import json
import os


class APIKey(ABC):
    @abstractmethod
    def api(self):
        '''
        Абстрактный класс для работы с API
        '''
        pass


class VacancyData(ABC):
    @abstractmethod
    def add_vacancy(self):
        '''
        Добавление вакансий в файл
        '''
        pass

    @abstractmethod
    def get_vacancy(self):
        '''
        Получение данных из файла по указанным критериям
        :return: data
        '''
        pass

    @abstractmethod
    def del_vacancy(self):
        '''
        Удаление информации о вакансиях
        '''
        pass


class HH(APIKey):

    def api(self):
        """
        Получение данных по ссылке, формат json
        :return: json файл
        """
        url_api = 'https://api.hh.ru/vacancies'
        params = {
            "text": "Python",
            "per_page": 10,
            "area": 113
        }
        return params, url_api


class SJ(APIKey):
    pass


class Vacancy:
    '''
    Класс для работы с вакансиями
    '''
    def __init__(self):
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)['items']

        self.title = json_data[0]['name']
        self.url = json_data[0]['url']
        self.payment = json_data[0]['salary']['from']
        self.requirement = json_data[0]['snippet']['requirement']
        self.responsibility = json_data[0]['snippet']['responsibility']

    def __le__(self, other):
        '''
        Сравнение вакансий по уровню зарплаты
        :param other: вакансия2
        :return: True - зп вакансии 1 меньше зп вакансии 2, в противном случае False
        '''
        return self.payment <= other.payment


class JSONDump(HH):
    '''
    Класс для сохранения информации о вакансиях в json файл
    '''
    def dump_j(self, params, url_api):
        response = requests.get(url_api, params=params)
        if response.status_code == 200:
            with open('vacancies.json', 'w') as f:
                json.dump(response.json(), f, indent=2, ensure_ascii=False)
        else:
            return f'Error: {response.status_code}'



