from models.db import get_db

class Attendance:
    @staticmethod
    def mark(roll, date, status):
        db = get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO attendance (roll_no, date, status)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (roll, date, status))

        db.commit()

    @staticmethod
    def percentage(roll):
        db = get_db()
        cur = db.cursor()

        # total classes
        cur.execute(
            "SELECT COUNT(*) FROM attendance WHERE roll_no=%s",
            (roll,)
        )
        total = cur.fetchone()[0]

        # present classes
        cur.execute(
            "SELECT COUNT(*) FROM attendance WHERE roll_no=%s AND status='Present'",
            (roll,)
        )
        present = cur.fetchone()[0]

        return round((present / total) * 100, 2) if total > 0 else 0
