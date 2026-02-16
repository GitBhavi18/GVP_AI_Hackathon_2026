from models.db import get_db

class Marks:
    @staticmethod
    def add_marks(roll, subject, marks):
        db = get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO marks (roll_no, subject, marks)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE marks = VALUES(marks)
        """, (roll, subject, marks))

        db.commit()
        cur.close()

    @staticmethod
    def average(roll):
        db = get_db()
        cur = db.cursor()

        cur.execute(
            "SELECT AVG(marks) FROM marks WHERE roll_no=%s",
            (roll,)
        )
        avg = cur.fetchone()[0]

        cur.close()
        return avg if avg else 0
