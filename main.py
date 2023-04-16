from src.item import HH, Vacancy, SJ, JSONDump

vac = SJ()
js = JSONDump(response=vac.api())
js.dump_js()
# vac1 = JSONDumpHH(SJ.api())


# py = Vacancy()
# print(py.title)
# print(py.payment)
# print(py.requirement)
# print(py.responsibility)