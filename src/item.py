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

    def api(self, keyword):
        """
        Подключение по API
        :return: response
        """
        url_api = 'https://api.hh.ru/vacancies'
        params = {
            "text": keyword,
            "per_page": 10,
            "area": 113
        }
        if requests.get(url_api, params=params).status_code == 200:
            return requests.get(url_api, params=params).json()['items']
        else:
            return f'Error: {requests.get(url_api, params=params).status_code}'

    def get_vacancies(self, keyword):
        return self.api(keyword)
     

class SJ(APIKey):
    def api(self, keyword):
        """
        Подключение по API
        :return: response
        """
        url_api = 'https://api.superjob.ru/2.0/vacancies/'
        params = {
            'keyword': keyword,
            'town': 'Москва',
            'count': 100,
            'period': 0
        }
        headers = {
            'X-Api-App-Id': 'v3.r.137494111.a6b43592ad3010404a6417932bb1b169d0bff73d.8da83ac6ac2fd9187fe1b5b8a7ecd1cc096ff71c',
            'Content-Type': 'application/json'
        }
        return requests.get(url_api, params=params, headers=headers).json()

    def get_vacancies(self, keyword):
        """
        Возвращает вакансии по ключевому слову
        :param keyword: ключевое слово пользователя
        """
        return self.api(keyword)


class Vacancy:
    """
    Класс для работы с вакансиями
    """
    def __init__(self, id_vac, title, url, payment_min, payment_max, currency, responsibility):
        self.id_vac = id_vac
        self.title = title
        self.url = url
        self.payment_max = payment_max
        self.payment_min = payment_min
        self.currency = currency
        self.responsibility = responsibility

    def __str__(self):
        """
        Вывод информации для пользователя
        """
        payment_min = f'от {self.payment_min}' if self.payment_min else ''
        payment_max = f'до {self.payment_max}' if self.payment_max else ''
        return f"{self.id_vac}\n{self.title}\n{self.url}\n{payment_min} {payment_max} {self.currency}" \
               f"\n{self.responsibility}"


class JSONDump:
    """
    Класс для сохранения информации о вакансиях в json файл
    """
    def __init__(self, response: requests):
        self.response = response

    def add_vacancy(self, data):
        """
        Запись данных в json файл
        """
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_vacancies_list_hh(self):
        """
        Создание списка экземпляров класса для платформы HH
        :return: список экземпляров класса
        """
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        vacancies = []
        for vacancy in data:
            if vacancy['salary'] is None:
                continue
            else:
                vacancies.append(
                    Vacancy(vacancy['id'], vacancy['name'], vacancy['alternate_url'], vacancy['salary']['from'],
                            vacancy['salary']['to'], vacancy['salary']['currency'],
                            vacancy['snippet']['responsibility']))
        return vacancies

    def get_vacancies_list_sj(self):
        """
        Создание списка экземпляров класса для платформы SJ
        :return: список экземпляров класса
        """
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)['objects']

        vacancies = []
        for vacancy in data:
            if vacancy['payment_from'] is None:
                continue
            else:
                vacancies.append(Vacancy(vacancy['id'], vacancy['profession'], vacancy['link'], vacancy['payment_from'],
                                         vacancy['payment_to'], vacancy['currency'], vacancy['candidat']))
        return vacancies

    def selected_top(self, data, top_n):
        """
        Выборка по вакансиям топ№ через платформу HH
        :param top_n: сколько вакансий вывести
        :return: список вакансий по условиям выборки
        """
        return data[:int(top_n)]

    def selected_payment_min(self, data, payment_min=None):
        """
        Выборка по вакансиям с зп не менее заданного уровня через платформу HH
        :param payment_min: минимальный уровень зп
        :return: список вакансий по условиям выборки
        """
        vacancies_payment = []
        if payment_min is not None:
            for i in data:
                if i.payment_min is not None:
                    if int(payment_min) <= int(i.payment_min):
                        vacancies_payment.append(i)
                    else:
                        continue
                else:
                    continue
        return vacancies_payment


    def delete_vacancy(self, vacancies, user_id=None):
        """
        Удаление экземпляра из списка по индексу, введенному пользователем
        :param vacancies: список экземпляров класса
        :param user_id: индекс, введенный пользователем
        :return: список вакансий без удаленного элемента
        """
        if user_id is not None:
            del vacancies[user_id-1]
            return vacancies

    def sorted_vac_min(self, data):
        """
        Сортировка json файла по минимальной зарплате
        :return: сортированный файл
        """
        for i in data:
            if i.payment_min is None:
                i.payment_min = 0
        return sorted(data, key=lambda x: x.payment_min, reverse=True)

    def get_vacancy(self, keyword):
        '''
        Получение данных из файла по указанным критериям
        :return: данные по критериям
        '''
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)['items']

        if keyword in json_data[0]['name']:
            return f"\n{json_data[0]['id']}\n{json_data[0]['name']}\n{json_data[0]['url']}\n{json_data[0]['salary']['from']}" \
                   f"\n{json_data[0]['snippet']['requirement']}\n{json_data[0]['snippet']['responsibility']} "

