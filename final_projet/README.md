
# 📌 Тема Итоговое задание по модулю 3

## 📌 Цель проекта
Проверить полученные знания и умения по дисциплине «ETL-процессы»
Научиться реализовывать ETL-процесс, используя инструменты Apache Airflow, PostgreSQL,  MongoDB

## 📌 Описание проекта

Этот проект реализует **ETL-процесс** с использованием **Apache Airflow, PostgreSQL и MongoDB**. Данные загружаются из **MongoDB**, очищаются и загружаются в **PostgreSQL**.

### 🔹 Используемые технологии

- **Apache Airflow** – для автоматизации ETL-процесса
- **PostgreSQL** – реляционная база данных
- **MongoDB** – NoSQL-хранилище данных
- **Docker** – контейнеризация сервисов

---

## 📌 Развёртывание проекта

### 🔹 1. Клонируем репозиторий

```bash
git clone https://github.com/andrey-osadchiy/etl_processes.git
```


### 🔹 2. Запускаем сервисы через Docker

```bash
docker-compose up -d
```

После запуска:

- **PostgreSQL** доступен на `localhost:5432`
- **MongoDB** доступен на `localhost:27017`
- **Airflow** доступен в браузере по адресу [http://localhost:8080](http://localhost:8080) (логин/пароль: `admin/admin`)

---

## 📌 Подготовка баз данных

### 🔹 1. Подключаемся к PostgreSQL 

```bash
docker exec -it postgres psql -U airflow -d airflow -f /sql/create_tables.sql
```
### 🔹 1.1 Cоздаём таблицы либо через файл create_tables либо руками в базе

![создание таблиц](https://raw.githubusercontent.com/andrey-osadchiy/etl_processes/main/final_projet/img/Снимок%20экрана%202025-03-15%20в%2018.16.20.png)

### 🔹 2. Генерируем тестовые данные в MongoDB

```bash
docker exec -it mongodb mongosh
```

```javascript
use etl_db;
db.students.insertMany([
    { _id: "s1", name: "Harry Potter", faculty: "Gryffindor" },
    { _id: "s2", name: "Draco Malfoy", faculty: "Slytherin" },
    { _id: "s3", name: "Hermione Granger", faculty: "Gryffindor" }
]);

db.subjects.insertMany([
    { _id: "sub1", name: "Defense Against the Dark Arts" },
    { _id: "sub2", name: "Charms" }
]);

db.marks.insertMany([
    { _id: "m1", student_id: "Harry Potter", subject_id: "Defense Against the Dark Arts", mark: 5 },
    { _id: "m2", student_id: "Draco Malfoy", subject_id: "Defense Against the Dark Arts", mark: 3 },
    { _id: "m3", student_id: "Hermione Granger", subject_id: "Charms", mark: 4 }
]);
```
![создание таблиц и их наполнение](https://raw.githubusercontent.com/andrey-osadchiy/etl_processes/main/final_projet/img/Снимок%20экрана%202025-03-15%20в%2018.19.41.png)


---

## 📌 Запуск ETL-процесса

### 🔹 1. Открываем Airflow и запускаем DAG

1. Переходим в [http://localhost:8080](http://localhost:8080)
2. Включаем DAG `etl_marks`
3. Жмакаем **Trigger DAG** для запуска
4. Смотрим, что всё ок
  
![эйрфлоу](https://raw.githubusercontent.com/andrey-osadchiy/etl_processes/main/final_projet/img/Снимок%20экрана%202025-03-15%20в%2019.44.14.png)

### 🔹 2. Проверяем данные в PostgreSQL

```sql
SELECT * FROM marks;
```

Если всё прошло успешно, таблица `marks` должна содержать записи! 🎉
![таблица marks](https://raw.githubusercontent.com/andrey-osadchiy/etl_processes/main/final_projet/img/Снимок%20экрана%202025-03-15%20в%2022.26.23.png)

---

