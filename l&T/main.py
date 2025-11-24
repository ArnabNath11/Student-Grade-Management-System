import json
import os

FILE = "students.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

def add_student():
    name = input("Enter student name: ")
    marks = int(input("Enter marks (0-100): "))
    grade = calculate_grade(marks)

    data = load_data()
    data.append({"name": name, "marks": marks, "grade": grade})
    save_data(data)

    print("\nStudent added successfully!\n")

def view_students():
    data = load_data()
    if not data:
        print("\nNo records found.\n")
        return

    print("\n--- Student Records ---")
    for s in data:
        print(f"Name: {s['name']}, Marks: {s['marks']}, Grade: {s['grade']}")
    print()

def menu():
    while True:
        print("===== Student Grade Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Try again.\n")

if __name__ == "__main__":
    menu()
