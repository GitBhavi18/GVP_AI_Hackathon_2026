import random
from models.student import Student

def generate_students():
    names = ["Aman", "Riya", "Neha", "Rahul"]
    for i in range(201, 205):
        Student.add_student(i, random.choice(names), random.randint(1, 6))
