# student_analytics.py
# Part A - Student Performance Analytics Module

from collections import defaultdict


def create_student(name: str, roll: str, **marks) -> dict:
    """Create a student record with flexible subject marks.

    Args:
        name: Full name of the student.
        roll: Roll number (e.g. 'R001').
        **marks: Keyword arguments for subject marks (e.g. math=85, python=92).

    Returns:
        A dict with keys: 'name', 'roll', 'marks', 'attendance'.

    Raises:
        ValueError: If name or roll is empty, or if any mark is outside 0-100.

    Example:
        >>> create_student('Amit', 'R001', math=85, python=92)
        {'name': 'Amit', 'roll': 'R001', 'marks': {'math': 85, 'python': 92}, 'attendance': 0.0}
    """
    if not name or not name.strip():
        raise ValueError("Student name cannot be empty.")
    if not roll or not roll.strip():
        raise ValueError("Roll number cannot be empty.")

    for subject, score in marks.items():
        if not isinstance(score, (int, float)):
            raise ValueError(f"Mark for '{subject}' must be a number.")
        if not (0 <= score <= 100):
            raise ValueError(f"Mark for '{subject}' must be between 0 and 100.")

    return {
        'name': name.strip(),
        'roll': roll.strip(),
        'marks': dict(marks),
        'attendance': 0.0
    }


def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """Calculate GPA from any number of marks.

    Args:
        *marks: Variable number of marks (floats or ints).
        scale: The GPA scale to use. Default is 10.0.

    Returns:
        GPA rounded to 2 decimal places.

    Raises:
        ValueError: If no marks are provided or scale is <= 0.

    Example:
        >>> calculate_gpa(85, 92, 78)
        8.5
    """
    if not marks:
        raise ValueError("At least one mark is required to calculate GPA.")
    if scale <= 0:
        raise ValueError("Scale must be a positive number.")

    avg = sum(marks) / len(marks)
    gpa = round((avg / 100) * scale, 2)
    return gpa


def get_top_performers(students: list, n: int = 5, subject: str = None) -> list:
    """Return top n students ranked by subject score or overall average.

    Args:
        students: List of student dicts.
        n: Number of top students to return. Default is 5.
        subject: Subject name to rank by. If None, uses overall average.

    Returns:
        List of top n student dicts sorted in descending order.

    Raises:
        ValueError: If n is less than 1.

    Example:
        >>> get_top_performers(students, n=1, subject='python')
        [{'name': 'Amit', ...}]
    """
    if not students:
        return []
    if n < 1:
        raise ValueError("n must be at least 1.")

    def sort_key(s):
        marks = s.get('marks', {})
        if not marks:
            return 0.0
        if subject:
            return marks.get(subject, 0)
        return sum(marks.values()) / len(marks)

    sorted_students = sorted(students, key=sort_key, reverse=True)
    return sorted_students[:n]


def generate_report(student: dict, **options) -> str:
    """Generate a formatted report string for a student.

    Args:
        student: A student dict with 'name', 'roll', 'marks', 'attendance'.
        **options: Optional keyword arguments:
            include_rank (bool): Include rank in report. Default True.
            include_grade (bool): Include letter grade. Default True.
            verbose (bool): Include detailed subject breakdown. Default False.

    Returns:
        A formatted report string.

    Raises:
        ValueError: If student dict is missing required keys.

    Example:
        >>> generate_report(student, include_grade=True, verbose=True)
        '--- Student Report ---\\nName: Amit ...'
    """
    required_keys = ['name', 'roll', 'marks']
    for key in required_keys:
        if key not in student:
            raise ValueError(f"Student record is missing required key: '{key}'")

    include_rank = options.get('include_rank', True)
    include_grade = options.get('include_grade', True)
    verbose = options.get('verbose', False)

    marks = student.get('marks', {})
    avg = sum(marks.values()) / len(marks) if marks else 0.0

    # Determine grade
    if avg >= 90:
        grade = 'A'
    elif avg >= 75:
        grade = 'B'
    elif avg >= 60:
        grade = 'C'
    else:
        grade = 'D'

    lines = ["--- Student Report ---"]
    lines.append(f"Name       : {student['name']}")
    lines.append(f"Roll       : {student['roll']}")
    lines.append(f"Attendance : {student.get('attendance', 0.0)}%")
    lines.append(f"Average    : {avg:.2f}")

    if include_grade:
        lines.append(f"Grade      : {grade}")

    if include_rank:
        lines.append("Rank       : Not computed (pass ranked list for rank)")

    if verbose:
        lines.append("Subject Breakdown:")
        for subj, score in marks.items():
            lines.append(f"  {subj.capitalize():<10}: {score}")

    lines.append("----------------------")
    return "\n".join(lines)


def classify_students(students: list) -> dict:
    """Classify students into grade buckets A, B, C, D based on average marks.

    Args:
        students: List of student dicts.

    Returns:
        A defaultdict with keys 'A', 'B', 'C', 'D', each containing a list of students.

    Example:
        >>> classify_students(students)
        {'A': [...], 'B': [...], 'C': [...], 'D': [...]}
    """
    result = defaultdict(list)

    if not students:
        return result

    for student in students:
        marks = student.get('marks', {})
        if not marks:
            result['D'].append(student)
            continue

        avg = sum(marks.values()) / len(marks)

        if avg >= 90:
            result['A'].append(student)
        elif avg >= 75:
            result['B'].append(student)
        elif avg >= 60:
            result['C'].append(student)
        else:
            result['D'].append(student)

    return result


# --- Quick demo when run directly ---
if __name__ == "__main__":
    students = [
        create_student('Amit', 'R001', math=85, python=92, ml=78),
        create_student('Priya', 'R002', math=95, python=88, ml=91),
        create_student('Rahul', 'R003', math=60, python=65, ml=58),
        create_student('Sneha', 'R004', math=72, python=70, ml=68),
        create_student('Karan', 'R005', math=45, python=50, ml=40),
    ]

    print("=== GPA Calculation ===")
    print(calculate_gpa(85, 92, 78))  # Expected: 8.5

    print("\n=== Top 1 by Python ===")
    top = get_top_performers(students, n=1, subject='python')
    print(top[0]['name'])  # Expected: Amit

    print("\n=== Top 2 Overall ===")
    top2 = get_top_performers(students, n=2)
    for s in top2:
        print(s['name'])

    print("\n=== Report ===")
    print(generate_report(students[0], include_grade=True, verbose=True))

    print("\n=== Classification ===")
    classified = classify_students(students)
    for grade, group in classified.items():
        print(f"{grade}: {[s['name'] for s in group]}")
