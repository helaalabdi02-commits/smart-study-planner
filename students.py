"""
Handles student registration, validation, and room allocation.

Students are stored using their registration number as the dictionary key.
"""

from typing import Dict, List, Optional

from models import Student

from hostel import (
    HostelLayout,
    room_exists,
    get_room,
    add_occupant,
    remove_occupant
)

StudentRegistry = Dict[str, Student]


# Check whether a registration number is already used
def registration_number_taken(
    students: StudentRegistry, reg_no: str
) -> bool:
    return reg_no in students


# Validate the basic details of a new student
def validate_new_student(
    name: str, reg_no: str, students: StudentRegistry
) -> Optional[str]:

    if not name.strip():
        return "Student name cannot be empty."

    if not reg_no.strip():
        return "Registration number cannot be empty."

    # Prevent duplicate registration numbers
    if registration_number_taken(students, reg_no):
        return f"Registration number '{reg_no}' is already in use."

    return None


# Validate and add a new student to the registry
def register_student(
    students: StudentRegistry,
    name: str,
    reg_no: str,
    gender: str,
    course: str,
    year: str,
    total_fee: float,
) -> bool:

    # Check the student's registration details first
    error = validate_new_student(name, reg_no, students)

    if error:
        print(f"Registration failed. {error}")
        return False

    # Create and store the new Student object
    students[reg_no] = Student(
        name=name.strip(),
        reg_no=reg_no.strip(),
        gender=gender.strip(),
        course=course.strip(),
        year=year.strip(),
        total_fee=total_fee,
    )

    print(
        f"Student registered successfully.\n"
        f"{name} ({reg_no}) added to the system."
    )

    return True


# Allocate a room or transfer the student to another room
def allocate_room(
    students: StudentRegistry,
    layout: HostelLayout,
    reg_no: str,
    block: str,
    room_no: str,
) -> bool:

    # Find the student before continuing
    student = students.get(reg_no)

    if student is None:
        print(
            f"Allocation failed. No student found with registration number {reg_no}."
        )
        return False

    # Make sure the selected room exists
    if not room_exists(layout, block, room_no):
        print(
            f"Allocation failed. Room {room_no} does not exist in {block}."
        )
        return False

    room = get_room(layout, block, room_no)

    # Do not allocate a room that has reached its capacity
    if not room.has_space():
        print("Allocation failed.")
        print(f"Room {room_no} is already full.")
        print(f"Capacity: {room.capacity}")
        print(f"Current occupancy: {len(room.occupants)}")
        return False

    # Remove the student from their old room when transferring.
    # Only do this if the student has a valid old block and room.
    if (
        student.is_allocated
        and student.block is not None
        and student.room is not None
        and room_exists(layout, student.block, student.room)
    ):
        remove_occupant(
            layout,
            student.block,
            student.room,
            reg_no
        )

    # Add the student to the new room
    add_occupant(
        layout,
        block,
        room_no,
        reg_no
    )

    # Update the student's room details
    student.block = block
    student.room = room_no

    print(f"{student.name} allocated to {block} - Room {room_no}.")

    print(
        f"Room {room_no} now has "
        f"{len(room.occupants)}/{room.capacity} occupants."
    )

    return True


# Find a student using their registration number
def find_by_registration(
    students: StudentRegistry, reg_no: str
) -> Optional[Student]:
    return students.get(reg_no)


# Find students whose names contain the search keyword
def find_by_name(
    students: StudentRegistry, keyword: str
) -> List[Student]:

    keyword_lower = keyword.strip().lower()

    return [
        s for s in students.values()
        if keyword_lower in s.name.lower()
    ]


# Display the main details of a student
def display_student(student: Student) -> None:

    print("\nStudent found:")
    print(f"Name: {student.name}")
    print(f"Reg No: {student.reg_no}")
    print(f"Course: {student.course}")
    print(f"Block: {student.block or '-'}")
    print(f"Room: {student.room or '-'}")
    print(f"Fees Paid: ${student.amount_paid}")
    print(f"Outstanding: ${student.balance}")