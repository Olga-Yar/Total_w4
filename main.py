from src.item import HH, SJ, Vacancy, JSONDump
from src.user_class import USER


def main():
    platform = input('Введите на какой платформе выполнить поиск (HH / SJ): ')
    keyword = input('Введите поисковый запрос: ')
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    payment_min = int(input('Введите минимальный уровень зп: '))
    user = USER(platform, keyword, top_n, payment_min)
    json_saver = JSONDump(user.keyword)
    if user.platform == 'HH':
        hh_api = HH()
        hh_vacancies = hh_api.get_vacancies(user.keyword)
        json_saver.add_vacancy(hh_vacancies)
        data = json_saver.selected_hh(user.top_n, user.payment_min)
        data = json_saver.sorted_vac_min(data)
        for row in data:
            print(row, end='\n\n')
        user_id = int(input('Удалить вакансию из списка по порядковому номеру: '))
        if user_id is not None:
            data = json_saver.delete_vacancy(data, user_id)
            for row in data:
                print(row, end='\n\n')
    elif user.platform == 'SJ':
        superjob_api = SJ()
        superjob_vacancies = superjob_api.get_vacancies(user.keyword)
        json_saver.add_vacancy(superjob_vacancies)
        data = json_saver.selected_sj(user.top_n)
        data = json_saver.sorted_vac_min(data)
        for row in data:
            print(row, end='\n\n')
        user_id = int(input('Удалить вакансию из списка по порядковому номеру: '))
        if user_id is not None:
            data = json_saver.delete_vacancy(data, user_id)
            for row in data:
                print(row, end='\n\n')
    else:
        print('Нет данных под ваш запрос.')

# Получение вакансий с разных платформ



# # Сохранение информации о вакансиях в файл







    # json_saver.delete_vacancy(data, 78473911)



if __name__ == "__main__":
    main()