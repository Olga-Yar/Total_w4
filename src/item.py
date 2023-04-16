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


class HH(APIKey):
    url_api = 'https://api.hh.ru/vacancies'

    def api(self):
        """
        Получение данных по ссылке, формат json
        :return: json файл
        """
        params = {
            "text": "Python",
            "per_page": 10,
            "area": 113
        }
        response = requests.get(self.url_api, params=params)
        if response.status_code == 200:
            with open('vacancies.json', 'w') as f:
                json.dump(response.json(), f, indent=2, ensure_ascii=False)
        else:
            return f'Error: {response.status_code}'


class Vacancy:
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






class SJ(APIKey):
    pass