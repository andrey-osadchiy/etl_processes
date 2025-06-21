# 📌Практическая работа (экзамен)
## 🔹Задание 1: Работа с Yandex DataTransfer
### Требуется перенести данные из Managed Service for YDB в объектное хранилище Object Storage. Выполнить необходимо с использованием сервиса Data Transfer.
1) Создаём бакет 
 ![Скриншот](screenshots/1.png)
2) Создаём базу данных YDB
![Скриншот](screenshots/2.png)
3) В YDB создаём таблицу (в моём случае таблица со списком моей семьи)
![Скриншот](screenshots/3.png)
4) Добавляем строки согласно инструкции
![Скриншот](screenshots/4.png)
5) Получилась такая таблица
![Скриншот](screenshots/5.png)
6)  Создаём эндпоинты (приёмник и источник) и запускаем трансфер
![Скриншот](screenshots/6.png)
![Скриншот](screenshots/06.png)
7)  Проверяем как прошел трансфер, заходим в ранее созданный нами бакет
![Скриншот](screenshots/7.png)
8)  Скачиваем файл, смотрим его содержимое.
![Скриншот](screenshots/8.png)
Всё как надо. Конечный файл лежит [тут](https://github.com/andrey-osadchiy/etl_processes/tree/main/final_project/staff)

## 🔹Задание 2: Автоматизация работы с Yandex Data Processing при помощи Apache AirFlow
### Требуется обрабатывать файлы (parquet или CSV) из внешнего источника. Размер входящих файлов меняется в различные дни месяца.  
Сначaла в ранее созданном бакете подготавливаем все необходимые папки. В папке dags будет лежать даг, в scripts наш скрипт. В папке файл наш файл со списком семьи из прошлого задания. В results мы засунем новый файл.
![Скриншот](screenshots/2/1.png)
Далее мы создаём кластеры. Кластер AirFlow, который будет аркестраротом (планирование и запуск) и Кластер Data Proc (непосредственное выполнение PySpark-заданий)

Сначла Data Proc
![Скриншот](screenshots/2/2.png)
Потом AirFlow
![Скриншот](screenshots/2/22.png)
Далее готовим файлы data_processing_dag.py 
```python

from airflow import DAG
from airflow.providers.yandex.operators.yandexcloud_dataproc import DataprocCreatePysparkJobOperator
from datetime import datetime

YC_DP_CLUSTER_ID = 'c9quhbgni0nl9loms74k'
YC_BUCKET = 'examen'

with DAG(
    'family_data_processing_v3',
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags=['data-processing']
) as dag:

    process_data = DataprocCreatePysparkJobOperator(
        task_id='process_data',
        cluster_id=YC_DP_CLUSTER_ID,
        main_python_file_uri=f's3a://{YC_BUCKET}/scripts/process_data.py',
        args=[
            '--input', f's3a://{YC_BUCKET}/file/family.csv',
            '--output', f's3a://{YC_BUCKET}/results/{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        ],
        properties={
            'spark.sql.legacy.timeParserPolicy': 'LEGACY',  # Для совместимости формата даты
            'spark.driver.memory': '2g'
        }
    )
```
![Скриншот](screenshots/2/4.png)

и process_data.py
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date
import sys

def main():
    spark = SparkSession.builder \
        .appName("FamilyDataProcessing") \
        .config("spark.hadoop.fs.s3a.endpoint", "storage.yandexcloud.net") \
        .getOrCreate()

    try:
        args = {k: v for k, v in zip(sys.argv[1::2], sys.argv[2::2])}
        input_path = args.get('--input', 's3://examen/file/family.csv')
        output_path = args.get('--output', 's3://examen/results/family_processed')
  
        df = spark.read.csv(input_path, header=False, schema="id INT, date STRING, name STRING, is_male BOOLEAN")
        
        # Преобразование даты (формат: "1993-04-14 00:00:00 +0000 UTC")
        df = df.withColumn("date", to_date(col("date").substr(1, 10), "yyyy-MM-dd"))
        
        # Проверка данных
        print("Пример данных:")
        df.show(5, truncate=False)
        
        # Фильтрация и агрегация
        result_df = df.filter(year(col("date")) >= 2001) \
                    .groupBy("is_male") \
                    .count()
        
        # Сохранение
        result_df.write.mode("overwrite").parquet(output_path)
        print(f"Результат сохранен в {output_path}")
        return 0

    except Exception as e:
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        return 1
    finally:
        spark.stop()

if __name__ == "__main__":
    sys.exit(main())
```
![Скриншот](screenshots/2/5.png)
Файлы можно посмотреть [тут](https://github.com/andrey-osadchiy/etl_processes/tree/main/final_project/staff)

Далее подключаемся к airflow по ранее нами созданным реквизитам
![Скриншот](screenshots/2/6.png)

Запускаем наш даг
![Скриншот](screenshots/2/7.png)
Всё успешно, проверяем папку с результатами:
![Скриншот](screenshots/2/8.png)
Отлично. Всё получилось. Осталось только удалить кластеры
![Скриншот](screenshots/9.png)


## 🔹Задание 4 (дополнительное): Визуализация в DataLens
### С помощью Yandex DataLens построить дашборды для визуализации загруженных данных. 
Создаём подключение к базе YDB где лежит наша таблица
![Скриншот](screenshots/4/1.png)
Создаём датасет
![Скриншот](screenshots/4/3.png)
На основании датасета создаём чарты,графики, диаграммы
![Скриншот](screenshots/4/4.png)
Создаём дашборд,  ознакомиться и поиграться с ним можно [тут](https://datalens.yandex.cloud/1mxcyr9l58xwm)
![Скриншот](screenshots/4/6.png)

## 🔹Задание 3: Работа с топиками Apache Kafka® с помощью PySpark-заданий в Yandex Data Processing
### Требуется настроить чтение топиков kafka для реализации потоковой аналитики
Логика такая: 
1) берем файл family.csv котоырй лежит в Object Storage
2) при помощи Kafka Producer читаем CSV из бакета (Преобразуем каждую строку в JSON.)
3) отправляем в Kafka-топик family-topic
4) Kafka Consumer слушает топик family-topic и для каждого сообщения парсит JSON и вставляет данные в YDB через UPSERT
5) по итогу данные появляются в таблице YDB family_members

Создаём таблицу в YDB кудп будет писаться информация


Создаём бакет со всеми файлами. тот который будет обрабатываться, а также 
kafka-write.py - забирает данные из CSV (Object Storage) и отправляет их в Kafka.
```python
import time
import random
import json
from kafka import KafkaProducer
import csv

# Настройка Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='rc1a-sp0t812fps48sn74.mdb.yandexcloud.net:9091',
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username='user1',
    sasl_plain_password='password1',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Чтение данных из CSV 
with open('gs://examen/kafka/family.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)  # Загружаем все строки

# Отправка данных в Kafka (по 1 записи в секунду)
while True:
    row = random.choice(data)  # Берём случайную строку
    id, birth_date, name_json, is_male = row
    message = {
        "id": id,
        "birth_date": birth_date,
        "first_name": json.loads(name_json)["first_name"],
        "is_male": is_male.lower() == "true"
    }
    producer.send('family-topic', value=message)
    print(f"Отправлено: {message}")
    time.sleep(1)  # Пауза 1 секунда
```
и kafka-read-ydb.py — читает данные из Kafka и сохраняет в YDB

```python
import json
from kafka import KafkaConsumer
import ydb
import os
from datetime import datetime

# Настройки YDB
driver_config = ydb.DriverConfig(
    endpoint="grpcs://ydb.serverless.yandexcloud.net:2135",
    database="/ru-central1/b1ga28ro2ctk606jpmoh/etnusig6loit8ui9gkmb",
    credentials=ydb.construct_credentials_from_environ(),  # Авторизация через IAM
)

# Настройки Kafka
consumer = KafkaConsumer(
    'family-topic',
    bootstrap_servers='ydb-03.serverless.yandexcloud.net:9093',
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-512',
    sasl_plain_username='user1',  
    sasl_plain_password='password1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Подключение к YDB
driver = ydb.Driver(driver_config)
driver.wait(fail_fast=True, timeout=5)
session = driver.table_client.session().create()

def upsert_family_member(data):
    query = f"""
    UPSERT INTO `family_members` (id, birth_date, first_name, is_male)
    VALUES (
        {data['id']},
        CAST('{data['birth_date']}' AS Timestamp),
        '{data['first_name']}',
        {data['is_male']}
    )
    """
    session.transaction().execute(query, commit_tx=True)

print("Ожидание данных из Kafka...")
for message in consumer:
    data = message.value
    print(f"Получено: {data}")
    upsert_family_member(data)
```
![Скриншот](screenshots/3/3.png)

Последним шагом создаём задание и запсукаем его
![Скриншот](screenshots/3/4.png)


Удаляем кластеры
![Скриншот](screenshots/3/5.png)
![Скриншот](screenshots/3/6.png)
