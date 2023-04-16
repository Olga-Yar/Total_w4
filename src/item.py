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
    def dump_j(self, params, url_api):
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
        Подключение по API
        :return: response
        """
        url_api = 'https://api.hh.ru/vacancies'
        params = {
            "text": "Python",
            "per_page": 10,
            "area": 113
        }
        response = requests.get(url_api, params=params)
        return response


class SJ(APIKey):
    def api(self):
        """
        Подключение по API
        :return: response
        """
        url_api = 'https://api.superjob.ru/2.0/vacancies/'
        params = {
            'keyword': 'Python',
            'town': 'Москва',
            'count': 100,
            'period': 0
        }
        headers = {
            'X-Api-App-Id': 'v3.r.137494111.a6b43592ad3010404a6417932bb1b169d0bff73d.8da83ac6ac2fd9187fe1b5b8a7ecd1cc096ff71c',
            'Content-Type': 'application/json'
        }
        response = requests.get(url_api, params=params, headers=headers)
        return response


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


class JSONDump():
    '''
    Класс для сохранения информации о вакансиях в json файл
    '''
    def __init__(self, response: requests):
        self.response = response

    def dump_js(self):
        if self.response.status_code == 200:
            with open('vacancies.json', 'w') as f:
                json.dump(self.response.json(), f, indent=2, ensure_ascii=False)
        else:
            return f'Error: {self.response.status_code}'


    # def get_vacancy(self, user_titlfe):
    #     '''
    #     Получение данных из файла по указанным критериям
    #     :return: данные по критериям
    #     '''
    #     with open('../vacancies.json', 'r', encoding='utf-8') as f:
    #         json_data = json.load(f)['items']
    #
    #     user_data = []
    #     for name in json_data[0]['name']:
    #         if user_title == name:
    #             user_data.append(json_data[0]['name'])
    #             user_data.append(json_data[0]['url'])
    #             user_data.append(json_data[0]['salary']['from'])
    #             user_data.append(json_data[0]['snippet']['requirement'])
    #             user_data.append(json_data[0]['snippet']['responsibility'])
    #     return user_data

#
# vac = JSONDump()
# vac1 = JSONDump.get_vacancy(vac, 'Python')
# print(vac1)



