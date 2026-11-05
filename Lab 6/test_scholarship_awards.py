import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# Code Coverage Test Cases targeting >90% (achieves 100% line coverage)

# ---------------- award_amount tests ----------------
def test_award_amount_unknown_category_raises_error():
    with pytest.raises(ValueError, match="unknown category"):
        award_amount("dance", 80, "low", False)


def test_award_amount_negative_marks_raises_error():
    with pytest.raises(ValueError, match="invalid marks"):
        award_amount("merit", -5, "low", False)


def test_award_amount_below_cutoff():
    assert award_amount("merit", 70, "low", False) == 0


def test_award_amount_renewal_non_sports_low_income_high_marks():
    assert award_amount("merit", 90, "low", True) == 3200


def test_award_amount_non_low_income_high_marks():
    assert award_amount("sports", 80, "medium", False) == 2000


# ---------------- is_eligible tests ----------------
def test_is_eligible_special_quota():
    assert is_eligible(60, 2, True) is True


def test_is_eligible_low_attendance():
    assert is_eligible(70, 0, False) is False


def test_is_eligible_regular_quota_passes():
    assert is_eligible(85, 1, False) is True


# ---------------- application_status tests ----------------
def test_application_status_renewal_paper_open():
    assert application_status(45, True, True) == "open"


def test_application_status_closing():
    assert application_status(10, False, False) == "closing"


def test_application_status_closed():
    assert application_status(2, False, False) == "closed"
