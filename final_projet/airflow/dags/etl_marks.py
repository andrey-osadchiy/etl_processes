from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymongo
import psycopg2

MONGO_CONN = "mongodb://mongodb:27017/"
mongo_client = pymongo.MongoClient(MONGO_CONN)
mongo_db = mongo_client["etl_db"]

PG_CONN = {
    "dbname": "airflow",
    "user": "airflow",
    "password": "airflow",
    "host": "postgres",
    "port": "5432"
}

# Функция для переноса данных
def transfer_data():
    conn = psycopg2.connect(**PG_CONN)
    cur = conn.cursor()

    # грузим факультеты
    faculties = mongo_db.students.distinct("faculty")
    cur.executemany("INSERT INTO faculties (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", [(f,) for f in faculties])

    # Загружаем студентов
    students = mongo_db.students.find()
    for student in students:
        cur.execute(
            """
            INSERT INTO students (name, faculty_id)
            VALUES (%s, (SELECT id FROM faculties WHERE name = %s))
            ON CONFLICT (name, faculty_id) DO NOTHING;
            """,
            (student["name"], student["faculty"])
        )

    # грузим предметы
    subjects = mongo_db.subjects.find()
    for subject in subjects:
        cur.execute(
            """
            INSERT INTO subjects (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
            """,
            (subject["name"],)
        )

    # оценки
    marks = mongo_db.marks.find()
    for mark in marks:
        print(f"Processing mark: {mark}")

        # Ищем ID студента по имени
        cur.execute("SELECT id FROM students WHERE name = %s;", (mark["student_id"],))
        student_result = cur.fetchone()

        # Ищем ID предмета по имени
        cur.execute("SELECT id FROM subjects WHERE name = %s;", (mark["subject_id"],))
        subject_result = cur.fetchone()

        print(f"Found student_id: {student_result}, subject_id: {subject_result}")

        # Если оба ID найдены, вставляем оценку
        if student_result and subject_result:
            student_id = student_result[0]
            subject_id = subject_result[0]

            cur.execute(
                """
                INSERT INTO marks (student_id, subject_id, mark)
                VALUES (%s, %s, %s)
                ON CONFLICT (student_id, subject_id) DO NOTHING;
                """,
                (student_id, subject_id, mark["mark"])
            )
        else:
            print(f"Skipping mark: student_id or subject_id not found for {mark}")


    conn.commit()
    cur.close()
    conn.close()

with DAG(
    "etl_marks",
    start_date=datetime(2024, 3, 15),
    schedule_interval="@daily",
    catchup=False
) as dag:
    transfer_task = PythonOperator(
        task_id="transfer_data",
        python_callable=transfer_data
    )

    transfer_task
