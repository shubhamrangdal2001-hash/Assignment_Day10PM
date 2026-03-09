# test_analytics.py
# Part A - Unit tests for student_analytics module

try:
    import pytest
except ImportError:
    # Minimal pytest stub so tests run without installing pytest
    import contextlib

    class _Raises:
        def __init__(self, exc):
            self._exc = exc
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, tb):
            if exc_type is None:
                raise AssertionError(f"Expected {self._exc.__name__} but no exception was raised.")
            if not issubclass(exc_type, self._exc):
                raise AssertionError(f"Expected {self._exc.__name__}, got {exc_type.__name__}.")
            return True  # suppress the expected exception

    class pytest:
        @staticmethod
        def raises(exc):
            return _Raises(exc)

from student_analytics import (
    create_student,
    calculate_gpa,
    get_top_performers,
    generate_report,
    classify_students,
)

# -----------------------------------------------
# Tests for create_student
# -----------------------------------------------

def test_create_student_basic():
    """Check that a basic student record is created correctly."""
    s = create_student('Amit', 'R001', math=85, python=92, ml=78)
    assert s['name'] == 'Amit'
    assert s['roll'] == 'R001'
    assert s['marks'] == {'math': 85, 'python': 92, 'ml': 78}
    assert s['attendance'] == 0.0

def test_create_student_flexible_subjects():
    """Check that **kwargs lets you pass any subjects."""
    s = create_student('Priya', 'R002', english=80, science=90)
    assert 'english' in s['marks']
    assert 'science' in s['marks']

def test_create_student_empty_name_raises():
    """Empty name should raise ValueError."""
    with pytest.raises(ValueError):
        create_student('', 'R001', math=80)

def test_create_student_empty_roll_raises():
    """Empty roll should raise ValueError."""
    with pytest.raises(ValueError):
        create_student('Amit', '', math=80)

def test_create_student_invalid_mark_raises():
    """Mark above 100 should raise ValueError."""
    with pytest.raises(ValueError):
        create_student('Amit', 'R001', math=150)

def test_create_student_negative_mark_raises():
    """Negative mark should raise ValueError."""
    with pytest.raises(ValueError):
        create_student('Amit', 'R001', math=-10)

# -----------------------------------------------
# Tests for calculate_gpa
# -----------------------------------------------

def test_calculate_gpa_basic():
    """Standard GPA calculation check."""
    result = calculate_gpa(85, 92, 78)
    assert result == 8.5

def test_calculate_gpa_perfect():
    """100 in all subjects should give GPA = scale."""
    result = calculate_gpa(100, 100, 100, scale=10.0)
    assert result == 10.0

def test_calculate_gpa_custom_scale():
    """Test with a 4.0 GPA scale."""
    result = calculate_gpa(80, 80, scale=4.0)
    assert result == 3.2

def test_calculate_gpa_no_marks_raises():
    """No marks should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_gpa()

def test_calculate_gpa_zero_scale_raises():
    """Scale of 0 should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_gpa(80, scale=0)

# -----------------------------------------------
# Tests for get_top_performers
# -----------------------------------------------

def test_get_top_performers_by_subject():
    """Amit has highest python score, should be first."""
    students = [
        create_student('Amit', 'R001', math=85, python=92, ml=78),
        create_student('Priya', 'R002', math=95, python=88, ml=91),
    ]
    top = get_top_performers(students, n=1, subject='python')
    assert top[0]['name'] == 'Amit'

def test_get_top_performers_overall():
    """Priya has higher overall average, should come first."""
    students = [
        create_student('Amit', 'R001', math=85, python=92, ml=78),
        create_student('Priya', 'R002', math=95, python=88, ml=91),
    ]
    top = get_top_performers(students, n=1)
    assert top[0]['name'] == 'Priya'

def test_get_top_performers_empty_list():
    """Empty student list should return empty list."""
    result = get_top_performers([], n=3)
    assert result == []

def test_get_top_performers_n_exceeds_list():
    """If n > list size, return all students."""
    students = [create_student('Amit', 'R001', math=85)]
    result = get_top_performers(students, n=10)
    assert len(result) == 1

def test_get_top_performers_invalid_n():
    """n < 1 should raise ValueError."""
    students = [create_student('Amit', 'R001', math=85)]
    with pytest.raises(ValueError):
        get_top_performers(students, n=0)

# -----------------------------------------------
# Tests for generate_report
# -----------------------------------------------

def test_generate_report_contains_name():
    """Report should include student name."""
    s = create_student('Amit', 'R001', math=85, python=92)
    report = generate_report(s)
    assert 'Amit' in report

def test_generate_report_with_grade():
    """Report with include_grade=True should show grade."""
    s = create_student('Priya', 'R002', math=95, python=88, ml=91)
    report = generate_report(s, include_grade=True)
    assert 'Grade' in report

def test_generate_report_verbose():
    """Verbose report should show individual subjects."""
    s = create_student('Amit', 'R001', math=85, python=92)
    report = generate_report(s, verbose=True)
    assert 'Math' in report or 'math' in report.lower()

def test_generate_report_missing_key_raises():
    """Missing 'marks' key should raise ValueError."""
    bad_student = {'name': 'Test', 'roll': 'R999'}
    with pytest.raises(ValueError):
        generate_report(bad_student)

# -----------------------------------------------
# Tests for classify_students
# -----------------------------------------------

def test_classify_students_grade_a():
    """Student with avg >= 90 should be in grade A."""
    students = [create_student('Priya', 'R002', math=95, python=88, ml=91)]
    result = classify_students(students)
    assert any(s['name'] == 'Priya' for s in result['A'])

def test_classify_students_grade_d():
    """Student with avg < 60 should be in grade D."""
    students = [create_student('Karan', 'R005', math=45, python=50, ml=40)]
    result = classify_students(students)
    assert any(s['name'] == 'Karan' for s in result['D'])

def test_classify_students_empty_list():
    """Empty input should return empty defaultdict."""
    result = classify_students([])
    assert len(result) == 0

def test_classify_students_multiple():
    """Multiple students should be split into correct grade buckets."""
    students = [
        create_student('A', 'R001', math=95),  # A
        create_student('B', 'R002', math=80),  # B
        create_student('C', 'R003', math=65),  # C
        create_student('D', 'R004', math=40),  # D
    ]
    result = classify_students(students)
    assert len(result['A']) == 1
    assert len(result['B']) == 1
    assert len(result['C']) == 1
    assert len(result['D']) == 1


if __name__ == "__main__":
    # Run a simple pass/fail summary without pytest
    import traceback
    tests = [
        test_create_student_basic,
        test_create_student_flexible_subjects,
        test_create_student_empty_name_raises,
        test_create_student_empty_roll_raises,
        test_create_student_invalid_mark_raises,
        test_create_student_negative_mark_raises,
        test_calculate_gpa_basic,
        test_calculate_gpa_perfect,
        test_calculate_gpa_custom_scale,
        test_calculate_gpa_no_marks_raises,
        test_calculate_gpa_zero_scale_raises,
        test_get_top_performers_by_subject,
        test_get_top_performers_overall,
        test_get_top_performers_empty_list,
        test_get_top_performers_n_exceeds_list,
        test_get_top_performers_invalid_n,
        test_generate_report_contains_name,
        test_generate_report_with_grade,
        test_generate_report_verbose,
        test_generate_report_missing_key_raises,
        test_classify_students_grade_a,
        test_classify_students_grade_d,
        test_classify_students_empty_list,
        test_classify_students_multiple,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"  FAIL  {t.__name__}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests.")
