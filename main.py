import json
from Classes import HeadHunterAPI, SuperJobAPI

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