from src.item import HH, Vacancy, SJ, JSONDump, USER

user = USER()

if user.platform == 'HH':
    vac = HH()
    js = JSONDump(response=vac.api())
    js.dump_js()
elif user.platform == 'SJ':
    vac = SJ()
    js = JSONDump(response=vac.api())
    js.dump_js()
else:
    print('Такой платформы нет')





# py = Vacancy()
# print(py.title)
# print(py.payment)
# print(py.requirement)
# print(py.responsibility)