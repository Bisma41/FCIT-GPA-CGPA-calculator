from tabulate import tabulate

def get_grade_and_points(percent):
    if 85 <= percent <= 100:
        return "A", 4.00
    elif 80 <= percent <= 84:
        return "A-", 3.70
    elif 75 <= percent <= 79:
        return "B+", 3.30
    elif 70 <= percent <= 74:
        return "B", 3.00
    elif 65 <= percent <= 69:
        return "B-", 2.70
    elif 61 <= percent <= 64:
        return "C+", 2.30
    elif 58 <= percent <= 60:
        return "C", 2.00
    elif 55 <= percent <= 57:
        return "C-", 1.70
    elif 50 <= percent <= 54:
        return "D", 1.00
    elif percent < 50:
        return "F", 0.00
    else:
        return "Invalid", None

def calculate_gpa(subjects, previous_cgpa=None, previous_total_credit_hours=0):
    total_points = 0
    total_credit_hours = 0
    result_table = []

    # Calculate total points and generate transcript data
    for subject in subjects:
        percent = subject['marks']
        credit_hours = subject['credit_hours']

        grade, points = get_grade_and_points(percent)
        if points is not None:
            subject_points = points * credit_hours
            total_points += subject_points
            total_credit_hours += credit_hours
            result_table.append([subject['name'], percent, grade, credit_hours, f"{points:.2f}"])
        else:
            print(f"Subject {subject['name']} has invalid grading (e.g., withdrawal or incomplete).")

    # Calculate Semester GPA
    semester_gpa = total_points / total_credit_hours if total_credit_hours > 0 else 0

    # Calculate CGPA if previous data exists
    if previous_cgpa is not None:
        total_points_cumulative = (previous_cgpa * previous_total_credit_hours) + total_points
        total_credit_hours_cumulative = previous_total_credit_hours + total_credit_hours
        cgpa = total_points_cumulative / total_credit_hours_cumulative
    else:
        cgpa = semester_gpa

   
    # Print the result table
    headers = ["Subject Name", "Marks (%)", "Grade", "Credit Hours", "Grade Points"]
    print("\nTranscript Summary:")
    print(tabulate(result_table, headers=headers, tablefmt="grid"))
    print("Total Credit Hours: ",f"{total_credit_hours}")
    print("GPA: ", f"{semester_gpa:.2f}","\t\t\t\t\t\t\tCGPA: ", f"{cgpa:.2f}")
    

    return semester_gpa, cgpa, total_credit_hours
    

def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

print("Welcome to GPA/CGPA Calculator!")
print("1. Calculate GPA for current semester")
print("2. Calculate CGPA (including previous semesters)")
print("3. Add marks of an improvement subject from previous semesters")

choice = get_valid_int("Enter your choice (1/2/3): ")

if choice == 1:
    # Option 1: GPA Calculation
    current_semester = get_valid_int("Enter the number of your current semester: ")
    num_subjects = get_valid_int("Enter the number of subjects in the current semester: ")
    subjects = []

    for i in range(num_subjects):
        subject_name = input(f"Enter the subject name for subject {i + 1}: ")

        while True:
            marks = get_valid_float(f"Enter the obtained marks for {subject_name}: ")
            if 0 <= marks <= 100:
                break
            print("Invalid marks. Please enter a value between 0 and 100.")

        while True:
            credit_hours = get_valid_float(f"Enter the credit hours for {subject_name}: ")
            if credit_hours > 0:
                break
            print("Invalid credit hours. Please enter a positive number.")

        subjects.append({'name': subject_name, 'marks': marks, 'credit_hours': credit_hours})

    if current_semester == 1:
        gpa, cgpa, total_credit_hours = calculate_gpa(subjects)
    else:
        previous_cgpa = get_valid_float("Enter your previous CGPA: ")
        previous_total_credit_hours = get_valid_float("Enter the total credit hours from previous semesters: ")
        gpa, cgpa, total_credit_hours = calculate_gpa(subjects, previous_cgpa, previous_total_credit_hours)

elif choice == 2:
    # Option 2: CGPA Calculation
    current_gpa = get_valid_float("Enter your current semester GPA: ")
    current_credit_hours = get_valid_float("Enter your current semester total credit hours: ")

    previous_gpas = []
    num_previous_semesters = get_valid_int("Enter the number of previous semesters: ")

    for i in range(num_previous_semesters):
        gpa = get_valid_float(f"Enter GPA for semester {i + 1}: ")
        credit_hours = get_valid_float(f"Enter total credit hours for semester {i + 1}: ")
        previous_gpas.append({'gpa': gpa, 'credit_hours': credit_hours})

    cgpa = calculate_cgpa(current_gpa, current_credit_hours, previous_gpas)
    print(f"\nYour CGPA is: {cgpa:.2f}")

elif choice == 3:
    # Option 3: Improvement Subject Handling
    num_previous_semesters = get_valid_int("Enter the number of previous semesters: ")
    previous_gpas = []

    for i in range(num_previous_semesters):
        gpa = get_valid_float(f"Enter GPA for semester {i + 1}: ")
        credit_hours = get_valid_float(f"Enter total credit hours for semester {i + 1}: ")
        previous_gpas.append({'gpa': gpa, 'credit_hours': credit_hours})

    add_subjects = []
    num_add_subjects = get_valid_int("Enter the number of improvement subjects: ")

    for i in range(num_add_subjects):
        subject_name = input(f"Enter the name of improvement subject {i + 1}: ")
        marks = get_valid_float(f"Enter the obtained marks for {subject_name}: ")
        credit_hours = get_valid_float(f"Enter the credit hours for {subject_name}: ")
        offered_semester = get_valid_int(f"Enter the semester this subject was offered in: ")
        was_failed = input(f"Was this subject failed previously? (yes/no): ").strip().lower()

        add_subjects.append({
            'name': subject_name,
            'marks': marks,
            'credit_hours': credit_hours,
            'semester': offered_semester,
            'was_failed': was_failed == 'yes'
        })

    for subject in add_subjects:
        semester_index = subject['semester'] - 1
        if 0 <= semester_index < len(previous_gpas):
            additional_credit_hours = 0 if subject['was_failed'] else subject['credit_hours']
            points = get_grade_and_points(subject['marks'])[1]
            total_points = previous_gpas[semester_index]['gpa'] * previous_gpas[semester_index]['credit_hours']
            total_points += points * subject['credit_hours']

            total_credit_hours = previous_gpas[semester_index]['credit_hours'] + additional_credit_hours
            updated_gpa = total_points / total_credit_hours if total_credit_hours > 0 else 0

            print(f"Updated GPA for Semester {subject['semester']} (after adding {subject['name']}): {updated_gpa:.2f}")
            previous_gpas[semester_index] = {'gpa': updated_gpa, 'credit_hours': total_credit_hours}
        else:
            print(f"Invalid semester number for subject {subject['name']}. Skipping.")

    calculate_cgpa_choice = input("Do you want to calculate CGPA after updating the semester(s)? (yes/no): ").strip().lower()
    if calculate_cgpa_choice == 'yes':
        current_gpa = get_valid_float("Enter your current semester GPA: ")
        current_credit_hours = get_valid_float("Enter your current semester total credit hours: ")

        cgpa = calculate_cgpa(current_gpa, current_credit_hours, previous_gpas)
        print(f"\nUpdated CGPA after improvement subjects: {cgpa:.2f}")

else:
    print("Invalid choice. Please select 1, 2, or 3.")
