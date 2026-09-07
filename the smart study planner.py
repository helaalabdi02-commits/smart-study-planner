# Smart Study Planner
# Programming Fundamentals Coursework

sessions = []


def classify_session(duration):
    """Classify a study session according to its duration."""

    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session():
    """Add a new study session."""

    print("\n--- Add Study Session ---")

    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day: ").strip()

    # Keep asking until the user enters a positive number.
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))

            if duration > 0:
                break
            else:
                print("Duration must be a positive number.")

        except ValueError:
            print("Please enter a valid number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)

    print("Study session added successfully!")


def view_sessions():
    """Display all recorded study sessions."""

    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print("-" * 85)
    print(
        f"{'Subject':<18}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Minutes':<10}"
        f"{'Class':<12}"
    )
    print("-" * 85)

    for session in sessions:
        classification = classify_session(session["duration"])

        print(
            f"{session['subject']:<18}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<10.1f}"
            f"{classification:<12}"
        )

    print("-" * 85)


def search_by_subject(subject):
    """Search for study sessions by subject."""

    found_sessions = []

    for session in sessions:
        if session["subject"].lower() == subject.lower():
            found_sessions.append(session)

    print(f"\n--- Search Results for {subject} ---")

    if not found_sessions:
        print("No sessions found for that subject.")
        return

    print("-" * 75)
    print(
        f"{'Subject':<18}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Minutes':<10}"
    )
    print("-" * 75)

    total_minutes = 0

    for session in found_sessions:
        print(
            f"{session['subject']:<18}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<10.1f}"
        )

        total_minutes += session["duration"]

    print("-" * 75)
    print(f"Total time spent on {subject}: {total_minutes:.1f} minutes")
    print(f"Total time in hours: {total_minutes / 60:.2f} hours")


def study_statistics():
    """Calculate and display study statistics."""

    print("\n--- Study Statistics ---")

    if not sessions:
        print("There are no study sessions to analyse.")
        return

    # Calculate total study time.
    total_minutes = sum(session["duration"] for session in sessions)

    print(f"Total hours studied overall: {total_minutes / 60:.2f} hours")

    # Calculate study time for each subject.
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]

        if subject not in subject_totals:
            subject_totals[subject] = 0

        subject_totals[subject] += session["duration"]

    print("\nTotal hours studied per subject:")

    for subject, minutes in subject_totals.items():
        print(f"{subject}: {minutes / 60:.2f} hours")

    # Find the subject with the least study time.
    weakest_subject = min(subject_totals, key=subject_totals.get)

    print(
        f"\nSubject with the least study time: "
        f"{weakest_subject} "
        f"({subject_totals[weakest_subject] / 60:.2f} hours)"
    )

    # Find the longest study session.
    longest_session = max(sessions, key=lambda session: session["duration"])

    print("\nLongest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")


def save_sessions():
    """Save all study sessions to study_log.txt."""

    try:
        with open("study_log.txt", "w") as file:

            for session in sessions:
                # Store each session using | as a separator.
                file.write(
                    f"{session['subject']}|"
                    f"{session['topic']}|"
                    f"{session['date']}|"
                    f"{session['duration']}\n"
                )

        print("Study sessions saved successfully.")

    except OSError:
        print("There was a problem saving the study sessions.")


def load_sessions():
    """Load existing study sessions from study_log.txt."""

    global sessions

    try:
        with open("study_log.txt", "r") as file:

            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if len(parts) == 4:
                    subject = parts[0]
                    topic = parts[1]
                    date = parts[2]

                    try:
                        duration = float(parts[3])

                        session = {
                            "subject": subject,
                            "topic": topic,
                            "date": date,
                            "duration": duration
                        }

                        sessions.append(session)

                    except ValueError:
                        # Ignore a damaged record instead of crashing.
                        continue

    except FileNotFoundError:
        # This is normal on the first run.
        sessions = []

    except OSError:
        print("There was a problem loading the study sessions.")


def main():
    """Run the Smart Study Planner."""

    load_sessions()

    print("=" * 50)
    print("       SMART STUDY PLANNER")
    print("=" * 50)

    while True:

        print("\nMenu")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()

        elif choice == "2":
            view_sessions()

        elif choice == "3":
            subject = input("Enter subject to search: ").strip()
            search_by_subject(subject)

        elif choice == "4":
            study_statistics()

        elif choice == "5":
            save_sessions()
            print("Thank you for using Smart Study Planner.")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()