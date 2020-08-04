### Итоговый проект курса "Машинное обучение в бизнесе"

Стек:
1. ML: sklearn, pandas, numpy
2. API: flask

Данные: https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv

Задача: предсказать по поведению покупателя его финансовую способность сделать что-то (не до конца пока понятно что, но это и не важно, наверное, пока что). Бинарная классификация

Используемые признаки:
1. SpecialDay (int)
2. Month (str:May, Jun, Feb etc.)
3. OperatingSystems (int)
4. Browser (int)
5. Region (int)
6. TrafficType (int)
7. VisitorType (str)
8. Weekend (bool: True/False)
9. Administrative (int)
10. Administrative_Duration (float)
11. Informational (int)
12. Informational_Duration (float)
13. ProductRelated (int)
14. ProductRelated_Duration (float)
15. BounceRates (float) 
16. ExitRates (float)
17. PageValues (float)


Преобразования: pipeline (get_dummies) 

Модель: random forest classifier

Процесс использования (проверки) модели:
- запустить run_server.py (фласк-сервер с моделью)
- запустить simple_request.py (запрос через api)

Что не сделано (или не доделано):
- Работа с фронт-ендом не доделана
- Работа с исключениями: что будет, если не подать в модель какие-то данные, или подать данные не того типа
- не до конца разобрался с пайплайном: приходится после подгрузки модели снова обучать пайплайн на создание дамми-признаков (сначала применять метод .fit), для чего пришлось подгружать тестовый датасет