import json
import requests
from heapq import nlargest
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


class Vacancies:
    all = []

    def __init__(self, name, link, salary_from, salary_to, description):
        self.name = name
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.all.append(self)
        self.max = 0
    def __str__(self):
        return self.name


    def __repr__(self):
        return f"{self.name} {self.salary_from}"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.salary_from + other.salary_from
        return None

    def __iter__(self):
        self.max = self.salary_from
        return self

    def __next__(self):
        if self.max < self.salary_from:
            self.max = self.salary_from
            return self.max
        else:
            raise StopIteration


    @classmethod
    def instantiate_from_json(cls):
        Vacancies.all.clear()
        with open("/home/dmitry/PycharmProjects/Cource_07.2023/test") as file:
            templates = json.load(file)
            for i in templates:
                name = i[0]
                link = i[1]
                salary_from = i[2]
                salary_to = i[3]
                description = i[4]
                vacancy = cls(name, link, salary_from, salary_to, description)
        return vacancy

a = Vacancies.instantiate_from_json()
c = []
max = int(input("Введите интересующую вас зп"))
for i in range(len(Vacancies.all)):

    if Vacancies.all[i].salary_from != None:
        if max < Vacancies.all[i].salary_from:
            print(f'{Vacancies.all[i].salary_from} {Vacancies.all[i].name}')
            c.append(Vacancies.all[i].salary_from)

d = nlargest(5, c)
print(d)

