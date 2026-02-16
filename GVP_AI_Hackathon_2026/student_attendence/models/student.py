from models.db import get_db

class Student:
    @staticmethod
    def add_student(roll, name, semester):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO student VALUES (%s,%s,%s)",
            (roll, name, semester)
        )
        db.commit()

    @staticmethod
    def get_all_students():
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM student")
        return cur.fetchall()

    @staticmethod
    def exists(roll):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT roll_no FROM student WHERE roll_no=%s", (roll,))
        return cur.fetchone() is not None
