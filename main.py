import json

from hostel import build_hostel_layout, display_occupancy, total_capacity, total_occupied
from students import register_student, allocate_room, find_by_registration, display_student
from fees import record_payment, display_payment_history
from reports import search_student, occupancy_report, fee_defaulters
from file_manager import load_data, save_data, data_file_exists
from activity_log import log_event


# Main menu
MENU = """
===== HOSTEL ROOM BOOKING SYSTEM =====
1. Register Student
2. Allocate / Transfer Room
3. Record Fee Payment
4. Search Student
5. Occupancy Report
6. Fee Defaulters
7. Student Details
8. Save Data
9. Exit
"""


# Get a valid amount
def ask_float(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount >= 0:
                return amount
            print("Amount cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")


# Load old data or create a new hostel
def start_up():
    if data_file_exists():
        try:
            return load_data()
        except json.JSONDecodeError:
            print("Saved data is damaged. Starting fresh.")

    return build_hostel_layout(), {}


# Register a student and allocate a room
def register_and_allocate(students, layout):
    print("\n--- Register Student ---")

    name = input("Name: ")
    reg_no = input("Registration number: ")
    gender = input("Gender: ")
    course = input("Course: ")
    year = input("Year: ")
    fee = ask_float("Total hostel fee: ")

    if not register_student(students, name, reg_no, gender, course, year, fee):
        return

    log_event("registration", f"{name} ({reg_no}) registered")

    block = input("Block: ")
    room = input("Room number: ")

    if allocate_room(students, layout, reg_no, block, room):
        log_event("allocation", f"{reg_no} allocated to {block} - {room}")


# Allocate or transfer a room
def allocate(students, layout):
    reg_no = input("Registration number: ")
    block = input("Block: ")
    room = input("Room number: ")

    if allocate_room(students, layout, reg_no, block, room):
        log_event("allocation", f"{reg_no} allocated to {block} - {room}")


# Record payment
def payment(students):
    reg_no = input("Registration number: ")
    student = find_by_registration(students, reg_no)

    if student is None:
        print("Student not found.")
        return

    amount = ask_float("Payment amount: ")

    if record_payment(student, amount):
        log_event("payment", f"{student.name} paid ${amount}")


# Search students
def search(students):
    keyword = input("Enter name or registration number: ")
    results = search_student(students, keyword)

    if not results:
        print("Student not found.")
        return

    for student in results:
        display_student(student)


# Save data
def save(layout, students):
    save_data(layout, students)

    occupied = total_occupied(layout)
    capacity = total_capacity(layout)

    log_event(
        "save",
        f"{len(students)} students, {occupied}/{capacity} beds occupied"
    )


# Start the program
def main():
    layout, students = start_up()
    display_occupancy(layout)

    while True:
        print(MENU)
        choice = input("Choose an option: ")

        if choice == "1":
            register_and_allocate(students, layout)

        elif choice == "2":
            allocate(students, layout)

        elif choice == "3":
            payment(students)

        elif choice == "4":
            search(students)

        elif choice == "5":
            block = input("Block name (Enter for all): ")
            occupancy_report(layout, block)

        elif choice == "6":
            threshold = ask_float("Minimum outstanding balance: ")
            fee_defaulters(students, threshold)

        elif choice == "7":
            search(students)

            # Payment history can be viewed separately when needed
            # through the fees module.

        elif choice == "8":
            save(layout, students)

        elif choice == "9":
            save(layout, students)
            print("Thank You")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()