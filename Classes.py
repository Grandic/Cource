import json
import requests
from abc import ABC, abstractmethod
from operator import attrgetter


class API(ABC):
    """Абстрактный класс с абстракт методом, который обязывает нас создать методы для работы с API для обоих
    наследников"""

    @abstractmethod
    def get_request(self, keyword):
        pass


class HeadHunterAPI(API):
    """Класс для работы с API HH.ru"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_request(self, keyword, page=0):
        """Метод запроса вакансий"""
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
        """Полученные данные с вакансиями итерируем и сохраняем в JSON файл для дальнейшей работы"""
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
    """Класс для работы с API SJ.ru"""

    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            "X-Api-App-Id": "v3.r.15956954.ef9ece301a81e1f04aa0ac0c905b9c497c445f45.035013f5924d01334a17d9c54856e6423a2b98a7"
        }

    def get_request(self, keyword, page=0):
        """Метод запроса вакансий"""
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
        """Полученные данные с вакансиями итерируем и сохраняем в JSON файл для дальнейшей работы"""
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


class JSON(ABC):
    """Абстрактный класс с абстракт методами, который обязывает нас создать методы для работы с JSON и экземплярами вакансий"""

    @abstractmethod
    def top_5_salary_from(self):
        pass

    @abstractmethod
    def top_5_salary_to(self):
        pass

    @abstractmethod
    def key_word_sort(self, key_word):
        pass

    @abstractmethod
    def salary_sort(self, salary):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def instantiate_from_json(self):
        pass


class Vacancies(ABC):
    """Класс для работы с файлом созданным одним из методов HH или SJ"""
    all = []
    def __init__(self, name, link, salary_from, salary_to, description):
        self.name = name
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.all.append(self)
        self.sort = [] # Атрибут, который будем использовать как строку для работы сортировки

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} c зарплатой от {self.salary_from} до {self.salary_to} ссылка на вакансию: {self.link}"

    def __add__(self, other):
        """Метод сравнения экземпляров класса по ЗП"""
        if isinstance(other, self.__class__):
            return self.salary_from + other.salary_from
        return None

    """Инициализируем экземпляры класса из списка вакансий полученных через API и сохранненых на PC"""

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

    def top_5_salary_from(self):
        """Метод вывода 5 топ зарплат от"""
        self.sort.clear()
        for i in range(self.all.__len__()):
            if self.all[i].salary_from is not None:
                self.sort.append(self.all[i])
        sort_by_salary_from = sorted(self.sort, key=lambda x: (x.salary_from), reverse=True)[:5]
        return sort_by_salary_from

    def top_5_salary_to(self):
        """Метод вывода 5 топ зарплат до"""
        self.sort.clear()
        for i in range(self.all.__len__()):
            if self.all[i].salary_to is not None:
                self.sort.append(self.all[i])
        sort_by_salary_to = sorted(self.sort, key=lambda x: x.salary_to, reverse=True)[:5]
        return sort_by_salary_to

    def key_word_sort(self, key_word):
        """Метод сортировки по ключевым словам"""
        self.sort.clear()
        k = key_word.split(",")
        for i in range(self.all.__len__()):
            for j in k:
                if self.all[i].description is not None and j in self.all[i].description:
                    self.sort.append(self.all[i])
        if len(self.sort) > 0:
            return self.sort
        else:
            return 'По данным ключевым словам вакансий не найдено'

    def salary_sort(self, salary):
        """Метод сортировки и показа вакансии по зп заданной пользователем"""
        self.sort.clear()
        k = salary.split("-")
        salary_from = int(k[0])
        salary_to = int(k[1])
        salary_middle = (salary_from+salary_to)/2 #Вычисляем среднее значение по вводу пользователя
        for i in range(self.all.__len__()):
            if self.all[i].salary_from is not None and int(salary_middle) <= int(self.all[i].salary_from):
                self.sort.append(self.all[i])
        if len(self.sort) > 0:
            return self.sort
        else:
            return 'Нет вакансий с указанной вами зарплатой'




