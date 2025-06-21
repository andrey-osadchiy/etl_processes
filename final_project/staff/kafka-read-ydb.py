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
    sasl_plain_username='user1',  # Замените на реальные
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