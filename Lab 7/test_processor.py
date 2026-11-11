from hypothesis import given, strategies as st
from processor import parse_applicant, marks_average, payable_award

@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        parse_applicant(s)
    except Exception as e:
        assert False, f"parse_applicant crashed with: {e}"

@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        marks_average(s)
    except Exception as e:
        assert False, f"marks_average crashed with: {e}"

@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        payable_award(s)
    except Exception as e:
        assert False, f"payable_award crashed with: {e}"

