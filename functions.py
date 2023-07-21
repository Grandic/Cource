from Classes import HeadHunterAPI, SuperJobAPI, Vacancies
import json

def to_json(Dictionary,f_name):
    """Функция записи любых данных работы класса Vacansies в JSON"""
    a = {}
    try:
        for i in Dictionary:
            a[i.name] = f'С зарплатой от {i.salary_from} до {i.salary_to}'
            to_js = json.dumps(a)
            with open(f_name, "w") as f:
                f.write(to_js)
    except AttributeError:
        print("Ошибка записи файла")

def user_interaction():
    """Основной цикл работы программы и взаимодейстивия ее с пользователем"""
    try:
        user_input = int(input("Приветствую Вас, где Вы хотите найти вакансии? 1: HH.RU 2: SJ.RU 3: Если хотите выйти из программы "))
        while True:
            if user_input == 1:
                print("Вы выбрали работу с HH\nВведите название интересующей вас вакансии: ")
                b = input()
                hh_api = HeadHunterAPI()
                hh_api.get_json(b)
                vacancies = Vacancies.instantiate_from_json()
                print("Вы можете выбрать следующие методы фильтрации вакансий:")
                print("1: Показать все вакансии")
                print("2: Отсортировать по ключевым словам в описании")
                print("3: Показать 5 самых высокооплачиваемых вакансий")
                print("4: Показать 5 вакансии с самой высокой базовой зарплатой")
                print("5: Показать вакансии с указанной Вами зарплатой")
                print("6: Закончить работу с программой")
                u_i = int(input())
                if u_i == 1:
                    print(f'Найденные вакансии: {vacancies.all}')
                    print("Новый поиск: 1")
                    print("Сохранить в файл вакансии с заданным Вами имененем: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        pass
                    elif u_i1 == 2:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения"))
                        to_json(vacancies.all, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 3:
                        print("Работа с программой завершена")
                        break
                elif u_i == 2:
                    try:
                        key = str(input("Введите желаемые слова для сортировки через запятую без пробелов"))
                        vacancies.key_word_sort(key)

                        print(f'Найденные вакансии: {vacancies.sort}')
                        print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                        print("Закончить работу с программой: 2")
                        print("Новый поиск: 3")
                        u_i1 = int(input())
                        if u_i1 == 1:
                            print("Вы выбрали сохранить результаты поиска")
                            t_j = str(input("Введите название файла для сохранения: "))
                            to_json(vacancies.sort, t_j)
                            print("Работа с программой завершена")
                            break
                        elif u_i1 == 2:
                            print("Работа с программой завершена")
                            break
                        elif u_i1 == 3:
                            continue
                    except ValueError:
                            print('Только буквы через запятую без пробелов')

                elif u_i == 3:
                    a = vacancies.top_5_salary_to
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Выбрать новую вакансию: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        continue
                    elif u_i1 == 3:
                        break

                elif u_i == 4:
                    a = vacancies.top_5_salary_from
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Выбрать новую вакансию: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        continue
                    elif u_i1 == 3:
                        break


                elif u_i == 5:
                    u_i2 = input("Введите интересующую вилку зарплаты через - без пробелов и запятых")
                    a = vacancies.salary_sort(u_i2)
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Закончить работу с программой: 2")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        print("Выбрать другую вакансию")

                elif u_i == 6:
                    break
            elif user_input == 2:
                b = input("Вы выбрали работу с SJ\nВведите название интересующей вас вакансии: ")
                sj_api = SuperJobAPI()
                sj_api.get_json(b)
                vacancies = Vacancies.instantiate_from_json()
                print("Вы можете выбрать следующие методы фильтрации вакансий:")
                print("1: Показать все вакансии")
                print("2: Сортировка по ключевым словам в описании")
                print("3: Показ 5 самых высокооплачиваемых вакансий")
                print("4: Показ 5 вакансий с самой высокой базовой зарплатой")
                print("5: Показ вакансий с указанной Вами зарплатой")
                print("6: Закончить работу с программой")
                u_i = int(input())
                if u_i == 1:
                    print(f'Найденные вакансии: {vacancies.all}')
                    print("Новый поиск: 1")
                    print("Сохранить в файл вакансии с заданным Вами имененем: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        pass
                    elif u_i1 == 2:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения"))
                        to_json(vacancies.all, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 3:
                        print("Работа с программой завершена")
                        break
                elif u_i == 2:
                    try:
                        key = str(input("Введите желаемые слова для сортировки через запятую без пробелов: "))
                        vacancies.key_word_sort(key)

                        print(f'Найденные вакансии: {vacancies.sort}')
                        print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                        print("Закончить работу с программой: 2")
                        print("Новый поиск: 3")
                        u_i1 = int(input())
                        if u_i1 == 1:
                            print("Вы выбрали сохранить результаты поиска")
                            t_j = str(input("Введите название файла для сохранения: "))
                            to_json(vacancies.sort, t_j)
                            print("Работа с программой завершена")
                            break
                        elif u_i1 == 2:
                            print("Работа с программой завершена")
                            break
                        elif u_i1 == 3:
                            continue
                    except ValueError:
                            print('Только буквы через запятую без пробелов')

                elif u_i == 3:
                    a = vacancies.top_5_salary_to
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Выбрать новую вакансию: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        continue
                    elif u_i1 == 3:
                        break

                elif u_i == 4:
                    a = vacancies.top_5_salary_from
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Выбрать новую вакансию: 2")
                    print("Закончить работу с программой: 3")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        continue
                    elif u_i1 == 3:
                        break


                elif u_i == 5:
                    u_i2 = input("Введите интересующую вилку зарплаты через - без пробелов и запятых: ")
                    a = vacancies.salary_sort(u_i2)
                    print(a)
                    print("Сохранить в файл вакансии с заданным Вами имененем: 1")
                    print("Закончить работу с программой: 2")
                    u_i1 = int(input())
                    if u_i1 == 1:
                        print("Вы выбрали сохранить результаты поиска")
                        t_j = str(input("Введите название файла для сохранения: "))
                        to_json(vacancies.sort, t_j)
                        print("Работа с программой завершена")
                        break
                    elif u_i1 == 2:
                        print("Выбрать другую вакансию")

                elif u_i == 6:
                    break

            elif user_input == 3:
                break
            else:
                print('Необходимо ввести число от 1 до 3')
                continue
    except ValueError:
        print('Необходимо вводить только ЧИСЛО от 1 до 3')