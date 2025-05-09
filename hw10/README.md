# Тема 10. Хранение данных в облаке
## Практическая работа
1. Создайте кластер-источник Managed Service for PostgreSQL 
2. Создайте эндпоинт-приемник типа Object Storage
3. Подготовьте и запустите трансфер
4. Проверьте работу копирования при повторной активации

Создаём кластер Managed Service и там создаём бд
 ![Скриншот](sreenschots/1.png)

Создаём там таблицу и заполняем её тестовыми данными
 ![Скриншот](sreenschots/2.png)
 ![Скриншот](sreenschots/3.png)

 Создаём эндпоинты (один на строне бд другой object storage)
 ![Скриншот](sreenschots/4.png)
 
 Создаём Data transfer
 ![Скриншот](sreenschots/6.png)
 ![Скриншот](sreenschots/7.png)

 
 Проверяем записалось ли в object storage 

 ![Скриншот](sreenschots/8.png)
