# Удаление дубликатов при вставке

## В students, subjects и marks используется ON CONFLICT DO NOTHING, чтобы избежать повторного добавления одних и тех же данных.

### 📌 Очистка дубликатов студентов:
```python
cur.execute(
    """
    INSERT INTO students (name, faculty_id)
    VALUES (%s, (SELECT id FROM faculties WHERE name = %s))
    ON CONFLICT (name, faculty_id) DO NOTHING;
    """,
    (student["name"], student["faculty"])
)
```
### 📌 Очистка дубликатов предметов:
```python

cur.execute(
    """
    INSERT INTO subjects (name)
    VALUES (%s)
    ON CONFLICT (name) DO NOTHING;
    """,
    (subject["name"],)
)
```

### 📌 Очистка дубликатов оценок
```python

cur.execute(
    """
    INSERT INTO marks (student_id, subject_id, mark)
    VALUES (%s, %s, %s)
    ON CONFLICT (student_id, subject_id) DO NOTHING;
    """,
    (student_id, subject_id, mark["mark"])
)

```
# Фильтрация отсутствующих данных (None в student_id или subject_id)
### 📌 DAG не вставляет оценки, если студент или предмет не найден в PostgreSQL
```python
if student_result and subject_result:
    student_id = student_result[0]
    subject_id = subject_result[0]
```
