from flask import Flask, render_template, request
from models.student import Student
from models.attendance import Attendance
from models.marks import Marks
from ai.ai_logic import attendance_warning, performance_remark
from flask import redirect, url_for
app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    students = Student.get_all_students()
    return render_template("home.html", students=students)

# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():
    roll = request.form["roll"]
    if Student.exists(roll):
        return "Roll number already exists <br><a href='/'>Go Back</a>"

    Student.add_student(
        roll,
        request.form["name"],
        request.form["semester"]
    )
    return "Student Registered <br><a href='/'>Go Back</a>"

# ---------------- NAVIGATION PAGES ----------------
from datetime import date
from models.db import get_db
from ai.ai_logic import attendance_warning

@app.route("/attendance")
def attendance_page():
    db = get_db()
    cur = db.cursor()

    today = date.today()

    cur.execute("""
        SELECT s.roll_no, s.name, s.semester,
               a.status,
               (SELECT COUNT(*) FROM attendance WHERE roll_no=s.roll_no) AS total,
               (SELECT COUNT(*) FROM attendance WHERE roll_no=s.roll_no AND status='Present') AS present
        FROM student s
        LEFT JOIN attendance a
        ON s.roll_no = a.roll_no AND a.date=%s
        ORDER BY s.roll_no
    """, (today,))

    rows = cur.fetchall()
    cur.close()

    students = []

    for r in rows:
        total = r[4]
        present = r[5]
        percent = round((present / total) * 100, 2) if total > 0 else 0
        warning = attendance_warning(percent)

        students.append((r[0], r[1], r[2], r[3], percent, warning))

    return render_template(
        "attendance.html",
        students=students,
        today=today
    )

from models.db import get_db

from ai.ai_logic import performance_remark

@app.route("/marks")
def marks_page():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT m.roll_no, m.subject, m.marks,
               (SELECT AVG(marks) FROM marks WHERE roll_no=m.roll_no) AS avg_marks
        FROM marks m
        ORDER BY m.id DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    cur.close()

    marks = []

    for r in rows:
        avg = r[3] if r[3] else 0
        remark = performance_remark(avg)
        marks.append((r[0], r[1], r[2], remark))

    return render_template("marks.html", marks=marks)



@app.route("/report")
def report_page():
    return render_template("report.html")

# ---------------- ATTENDANCE SUBMIT ----------------
@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    Attendance.mark(
        request.form["roll"],
        request.form["date"],
        request.form["status"]
    )
    return redirect(url_for("attendance_page"))

# ---------------- MARKS SUBMIT ----------------
@app.route("/enter_marks", methods=["POST"])
def enter_marks():
    Marks.add_marks(
        request.form["roll"],
        request.form["subject"],
        request.form["marks"]
    )
    return "Marks Saved <br><a href='/marks'>Go Back</a>"

# ---------------- VIEW REPORT ----------------
@app.route("/view_report", methods=["POST"])
def view_report():
    roll = request.form["roll"]

    student = Student.get_by_roll(roll)
    if not student:
        return "Student not found <br><a href='/report'>Go Back</a>"

    attendance = Attendance.percentage(roll)
    avg = Marks.average(roll)

    remark = performance_remark(avg)
    warning = attendance_warning(attendance)

    return render_template(
        "report.html",
        student=student,
        attendance=attendance,
        avg=avg,
        remark=remark,
        warning=warning
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
