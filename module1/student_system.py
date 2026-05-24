import json

# ==================
# FUNCTIONS
# ==================

def add_student(students, student_id, name, marks):
    students[student_id] = {
        "name": name,
        "marks": marks,
        "grade": calculate_grade(marks)
    }
    print(f"✅ {name} add ho gaya!")

def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    else:
        return "Fail"

def save_data(students):
    with open("results.json", "w") as file:
        json.dump(students, file, indent=4)
    print("💾 Data saved!")

def load_data():
    try:
        with open("results.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("📂 Koi purana data nahi — fresh start!")
        return {}

def show_all(students):
    if not students:
        print("Koi student nahi hai abhi.")
        return
    print("\n--- Sare Students ---")
    for sid, info in students.items():
        print(f"{sid}: {info['name']} | Marks: {info['marks']} | Grade: {info['grade']}")

def class_average(students):
    if not students:
        print("Koi student nahi!")
        return
    all_marks = [info["marks"] for info in students.values()]
    avg = sum(all_marks) / len(all_marks)
    print(f"\n📊 Class Average: {avg:.1f}")

# ==================
# MAIN PROGRAM
# ==================

students = load_data()  # Pehle purana data load karo

while True:
    print("\n=== Student Result System ===")
    print("1. Student add karo")
    print("2. Sab dekho")
    print("3. Average dekho")
    print("4. Save karo")
    print("5. Quit")

    choice = input("Option choose karo: ")

    if choice == "1":
        sid = input("Student ID (jese s001): ")
        name = input("Name: ")
        try:
            marks = int(input("Marks (0-100): "))
            add_student(students, sid, name, marks)
        except ValueError:
            print("❌ Marks mein sirf number daalo!")

    elif choice == "2":
        show_all(students)

    elif choice == "3":
        class_average(students)

    elif choice == "4":
        save_data(students)

    elif choice == "5":
        save_data(students)
        print("Khuda Hafiz!")
        break

    else:
        print("❌ Galat option!")