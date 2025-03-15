CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) UNIQUE
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(40),
    faculty_id INT REFERENCES faculties(id)
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) UNIQUE
);

CREATE TABLE marks (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id),
    subject_id INT REFERENCES subjects(id),
    mark INT CHECK (mark BETWEEN 1 AND 5)
);

ALTER TABLE students ADD CONSTRAINT unique_student UNIQUE (name, faculty_id);
ALTER TABLE subjects ADD CONSTRAINT unique_subject UNIQUE (name);
ALTER TABLE marks ADD CONSTRAINT unique_mark UNIQUE (student_id, subject_id);