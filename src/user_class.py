# Функция для взаимодействия с пользователем
class USER:

    def __init__(self, platform='HH', keyword='Python', top_n=100, payment_min=100000):
        self.platform = platform
        self.keyword = keyword
        self.top_n = top_n
        self.payment_min = payment_min



#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
#
#     if not filtered_vacancies:
#         print("Нет вакансий, соответствующих заданным критериям.")
#         return
#
#     sorted_vacancies = sort_vacancies(filtered_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
