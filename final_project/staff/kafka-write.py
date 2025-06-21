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