from abc import ABC, abstractmethod
import requests
import json
import os


class APIKey(ABC):
    @abstractmethod
    def api(self):
        pass


class HH(APIKey):
    url_api = 'https://api.hh.ru/vacancies'

    def api(self):
        """
        Получение данных по ссылке, формат json
        :return: json файл
        """
        params = {
            "text": "Python-разработчик",
            "per_page": 10,
            "area": 113
        }
        response = requests.get(self.url_api, params=params)
        if response.status_code == 200:
            with open('vacancies.json', 'w', encoding='UTF-8') as f:
                json.dump(response.json(), f)
        else:
            return f'Error: {response.status_code}'





class SJ(APIKey):
    pass