# Тема 11. Работа с облачными вычислениями
## Практическая работа
### Описание задания
Повторите работу из демонстрации вебинара «Работа с облачными вычислениями».
Обработайте данные из Yandex Object Storage с помощью сервиса Yandex Apache AirFlow, используя мощности Yandex Data Processing.

Создаём необходимые папки в бакете и кладём туда два файла согласно инструкции 
 ![Скриншот](screenshots/2.png)
 ![Скриншот](screenshots/3.png)

 Далее создаём сеть и настраиваем подсети, предварительно создав nat-шлюз и настроив таблицы маршрутизации
![Скриншот](screenshots/4.png)
![Скриншот](screenshots/7.png)

 Далее создаём кластер Metastore
![Скриншот](screenshots/5.png)
![Скриншот](screenshots/6.png)

 Создаём и запускаем кластер через Yandex Managed Service for Apache Airflow
 ![Скриншот](screenshots/1.png)

Залогиниваемся в Apache Airflow под реквизтами указанными нами во время настройки кластера
 ![Скриншот](screenshots/9.png)
Запускаем Dag
 ![Скриншот](screenshots/8.png)

Выключаем кластер
 ![Скриншот](screenshots/01.png)
