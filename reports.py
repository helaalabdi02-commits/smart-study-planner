from models import Student


# Search for a student using registration number or name
def search_student(students, keyword):

    # First check if the keyword is a registration number
    student = students.get(keyword)

    if student is not None:
        return [student]

    # If it is not a registration number, search by name
    keyword = keyword.strip().lower()

    results = []

    # Check each student's name for a match
    for student in students.values():
        if keyword in student.name.lower():
            results.append(student)

    return results


# Display hostel occupancy
def occupancy_report(layout, block_filter=""):

    print("\n========== HOSTEL OCCUPANCY REPORT ==========")

    # If a block was entered, show only that block
    if block_filter:

        # Make sure the requested block exists
        if block_filter not in layout:
            print(f"\nNo block named '{block_filter}' was found.")
            return

        blocks_to_show = {
            block_filter: layout[block_filter]
        }

    else:
        # No filter means show every block
        blocks_to_show = layout

    # Go through each selected block
    for block_name, rooms in blocks_to_show.items():

        print(f"\n{block_name.upper()}")

        # Display the occupancy and status of each room
        for room_no, room in rooms.items():

            status = "FULL" if room.is_full() else "AVAILABLE"

            print(
                f"{room_no}: "
                f"{len(room.occupants)}/{room.capacity} - {status}"
            )


# Display students who still owe money
def fee_defaulters(students, threshold):

    print("\n========== FEE DEFAULTERS ==========\n")

    defaulters = []

    # Check every student against the balance threshold
    for student in students.values():

        balance = student.get_balance()

        if balance >= threshold:
            defaulters.append(student)

    # Put students with the highest balance first
    defaulters.sort(
        key=lambda student: student.get_balance(),
        reverse=True
    )

    # Stop if nobody meets the threshold
    if not defaulters:
        print("No students at or above this threshold.")
        return

    # Display each student who still owes money
    for student in defaulters:

        print(
            f"{student.name:<15} "
            f"{student.reg_no:<12} "
            f"Outstanding: ${student.get_balance()}"
        )