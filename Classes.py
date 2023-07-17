import csv
import json
import requests
import time
import os
from abc import ABC, abstractmethod


class API(ABC):
    @abstractmethod
    def get_request(self, keyword):
        pass


class HeadHunterAPI(API):
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_request(self, keyword, page=0):
        self.params = {'text': keyword,
                       'area': 1,
                       'page': page,
                       'per_page': 100,
                       'archived': False,
                       'only_with_salary': True
                       }
        req = requests.get(self.url, self.params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    def get_json(self, name):
        result = []
        for page in range(0, 5):
            # Преобразуем текст ответа запроса в справочник Python
            file = json.loads(self.get_request(name, page))
            for i in file['items']:
                i_name = i.get('name')
                i_link = i.get('alternate_url')
                work = i.get('snippet')
                i_work = work.get('requirement')
                salary = i.get('salary')
                j_payment_from = salary.get('from')
                j_payment_to = salary.get('to')
                result.append([i_name, i_link, j_payment_from, j_payment_to, i_work])
        with open("test", "w", encoding='utf-8') as file:
            json.dump(result, file)


class SuperJobAPI(API):
    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            "X-Api-App-Id": "v3.r.15956954.ef9ece301a81e1f04aa0ac0c905b9c497c445f45.035013f5924d01334a17d9c54856e6423a2b98a7"
        }

    def get_request(self, keyword, page=0):
        self.params = {
            "count": 100,
            "page": page,
            "keyword": keyword,
            "archive": False,
            "no_agreement": 1,
            "town": 4
        }
        req = requests.get(self.url, headers=self.headers, params=self.params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data

    def get_json(self, name):
        result = []
        for page in range(0, 5):
            # Преобразуем текст ответа запроса в справочник Python
            file = json.loads(self.get_request(name, page))
            for i in file['objects']:
                i_name = i.get('profession')
                i_link = i.get('link')
                i_payment_from = i.get('payment_from')
                i_payment_to = i.get('payment_to')
                i_work = i.get('candidat')
                result.append([i_name, i_link, i_payment_from, i_payment_to, i_work])
        with open("test", "w", encoding='utf-8') as file:
            json.dump(result, file)

a = input("Добрый вечер, где хотите провести поиск вакансии? 1: HH.RU 2: SJ")
while True:
    if a == 1:
        b = input("Вы выбрали работу с HH\nВведите название интересующей вас вакансии")
        hh_api = HeadHunterAPI()
        hh_vacancies = hh_api.get_json(b)
        with open("/home/dmitry/PycharmProjects/Cource_07.2023/test") as file:
            templates = json.load(file)
            count = 0

            for i in templates:
                if i[3] != None:
                    if int(i[3]) > count:
                        count = i[3]
                        name = i[0]
                        desc = i[4]
            print(f'В данный момент максимальная зарплата вакансии {name} равна {count} {desc}')
    elif a == 2:
        b = input("Вы выбрали работу с SJ\nВведите название интересующей вас ваканси")
        superjob_api = SuperJobAPI()
        superjob_vacancies = superjob_api.get_json(b)
        with open("/home/dmitry/PycharmProjects/Cource_07.2023/test") as file:
            templates = json.load(file)
            count = 0
            for i in templates:
                if i[3] != None:
                    if int(i[3]) > count:
                        count = i[3]
                        name = i[0]
                        desc = i[4]

            print(f'В данный момент максимальная зарплата вакансии {name} равна {count} {desc}')
    else:
            print('Необходимо ввести число от 1 до 2')
            a = int(input())
            continue


#
# with open("/home/dmitry/PycharmProjects/Cource_07.2023/test") as file:
#     templates = json.load(file)
#     count = 0
#     for i in templates:
#         if i[3] > count:
#             count = i[3]
#             name = i[0]
#     print(f'В данный момент максимальная зарплата вакансии {name} равна {count}')
