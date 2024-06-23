import sqlite3

# Create a SQLite database and define tables
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject TEXT,
    grade REAL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
''')

connection.commit()


# Define the University class
class University:
    def __init__(self, name):
        self.name = name

    def add_student(self, name, age):
        cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
        connection.commit()

    def add_grade(self, student_id, subject, grade):
        cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
        connection.commit()

    def get_students(self, subject=None):
        if subject is None:
            cursor.execute(
                "SELECT students.name, students.age, grades.subject, grades.grade FROM students JOIN grades ON students.id = grades.student_id")
        else:
            cursor.execute(
                "SELECT students.name, students.age, grades.subject, grades.grade FROM students JOIN grades ON students.id = grades.student_id WHERE grades.subject=?",
                (subject,))

        return cursor.fetchall()


# Create an instance of the University class
u1 = University('Urban')

u1.add_student('Ivan', 26)  # id - 1
u1.add_student('Ilya', 24)  # id - 2

u1.add_grade(1, 'Python', 4.8)
u1.add_grade(2, 'PHP', 4.3)

# Add more students and grades
student_data = [
    ('Alex', 22),
    ('Olga', 25),
    ('Nikita', 23),
    ('Elena', 21)
]

for student in student_data:
    u1.add_student(student[0], student[1])

grades_data = [
    (1, 'Python', 4.5),
    (1, 'Databases', 4.2),
    (2, 'PHP', 4.1),
    (2, 'Web Development', 4.4),
    (3, 'Python', 4.7),
    (3, 'Algorithms', 4.8),
    (4, 'Database Design', 4.6),
    (4, 'Java Programming', 4.3)
]

for grade in grades_data:
    u1.add_grade(grade[0], grade[1], grade[2])

# Retrieve and print student information
print(u1.get_students())
print(u1.get_students('Python'))
