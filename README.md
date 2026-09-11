# Hostel Room Booking System

A console-based Python application for hostel registration, room
allocation, fee payments, search and reporting. Nothing about the
hostel's structure or fee amounts is hardcoded - the block layout is
defined by whoever runs the program the first time it starts, and each
student's total fee is entered at registration.

## Running

    python3 main.py

Requires Python 3.9+. No external libraries are needed.

## First run

Since there's no saved data yet, the program asks you to define the
hostel: how many blocks, what each is called, how many rooms per block,
and each room's capacity. This only happens once - after that, the
layout is loaded from hostel_data.json automatically.

## Menu

    1. Register Student (includes Room Allocation)
    2. Allocate / Transfer Room
    3. Record Fee Payment
    4. Search Student
    5. View Occupancy Report
    6. View Fee Defaulters
    7. View Student Details
    8. Save Data
    9. Exit

Registering a student (option 1) asks for their room in the same step -
no separate menu trip needed. If the room given turns out to be full or
doesn't exist, the student is still registered; option 2 places them
once a room is available, or transfers an already-housed student
elsewhere.

Both "View Occupancy Report" (5) and "View Student Details" (7) accept
a search term: a block name for the occupancy report (blank = all
blocks), and a name or registration number for student details. A
search that matches nothing always prints a clear message.

## IMPORTANT: saving

Nothing is written to disk until you choose option 8 (Save Data) or
option 9 (Exit) - both save. Everything before that only exists in
memory for the current run. If you close the terminal window directly,
or the program crashes partway through, whatever hasn't been saved yet
is lost. This is a normal, expected trade-off for a program that
doesn't save after every single keystroke - just make sure you save (or
exit properly) before closing.

## Files produced while running

- **hostel_data.json** - the current state: every block, room, student
  and payment. Each room's entry includes two derived fields, recalculated
  fresh on every save:
    - `"occupied"` - true the instant a room has even one student in it.
      Check this to confirm an allocation actually took effect.
    - `"status"` - `"FULL"` only once the room hits capacity,
      `"AVAILABLE"` otherwise. This answers a different question (can
      it take another student) than `"occupied"` does.
  This file is fully overwritten on every save - it only ever reflects
  the latest state.
- **activity_log.json** - a permanent, append-only history of every
  registration, allocation, payment and save, each with a timestamp.
  Unlike hostel_data.json, this file is never overwritten - only added
  to - so opening it later shows the full timeline of everything that's
  happened, even for students or allocations that have since changed.

## Files

- main.py            Entry point, menu loop, first-run setup, activity logging
- models.py           Room / Student / Payment dataclasses
- hostel.py           Hostel layout setup and room operations
- students.py         Registration, validation, allocation
- fees.py              Fee payments and history
- reports.py          Search, occupancy report (with block filter), fee defaulters
- file_manager.py    Saving/loading hostel_data.json
- activity_log.py     Permanent append-only record of every action
