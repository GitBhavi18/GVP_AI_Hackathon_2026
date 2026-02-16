def attendance_warning(percent):
    if percent < 75:
        return "⚠ Attendance Shortage"
    return "Attendance OK"

def performance_remark(avg_marks):
    if avg_marks >= 75:
        return "Good"
    elif avg_marks >= 50:
        return "Average"
    else:
        return "Needs Improvement"
