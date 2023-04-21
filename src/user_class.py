# Функция для взаимодействия с пользователем
class USER:

    def __init__(self, platform='HH', keyword='Python', top_n=100, payment_min=100000):
        self.platform = platform
        self.keyword = keyword
        self.top_n = top_n
        self.payment_min = payment_min

