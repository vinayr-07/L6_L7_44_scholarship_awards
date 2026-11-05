import pytest
from scholarship_awards import award_amount, is_eligible, application_status


class TestBranchCoverageScholarshipAwards:
    """Comprehensive branch coverage tests targeting 100% branch and decision coverage."""

    # =========================================================================
    # Function 1: award_amount(category, marks, income_level, is_renewal)
    # =========================================================================

    def test_award_amount_category_not_in_cutoff_marks(self):
        # Branch: category not in CUTOFF_MARKS -> True (raises ValueError)
        with pytest.raises(ValueError, match="unknown category"):
            award_amount("dance", 80, "low", False)

    def test_award_amount_negative_marks(self):
        # Branch: marks < 0 -> True (raises ValueError)
        with pytest.raises(ValueError, match="invalid marks"):
            award_amount("merit", -1, "low", False)

    def test_award_amount_renewal_non_sports_cutoff_reduction(self):
        # Branch: is_renewal=True and category != "sports" -> True
        # category="arts" (cutoff 65 -> 60), marks=70 (above=10 <= 15)
        # income_level="low" (rate=100). above <= 15 (skips rate increase)
        # expected = 10 * 100 = 1000
        assert award_amount("arts", 70, "low", True) == 1000

    def test_award_amount_renewal_sports_no_reduction(self):
        # Branch: is_renewal=True and category == "sports" (category != "sports" evaluates to False)
        # cutoff stays 60. marks=70 (above=10 <= 15).
        # income_level != "low" (rate=60).
        # expected = 10 * 60 = 600
        assert award_amount("sports", 70, "high", True) == 600

    def test_award_amount_non_renewal(self):
        # Branch: is_renewal=False (skips cutoff reduction)
        # category="merit" (cutoff=75). marks=85 (above=10 <= 15).
        # income_level="low" (rate=100).
        # expected = 10 * 100 = 1000
        assert award_amount("merit", 85, "low", False) == 1000

    def test_award_amount_above_less_than_or_equal_to_zero(self):
        # Branch: above <= 0 -> True (returns 0)
        # Exact cutoff: merit (cutoff 75), marks=75 => above=0
        assert award_amount("merit", 75, "low", False) == 0
        # Below cutoff: merit (cutoff 75), marks=60 => above=-15
        assert award_amount("merit", 60, "low", False) == 0

    def test_award_amount_high_marks_tier_low_income(self):
        # Branch: above > 15 -> True AND income_level == "low" -> True
        # merit cutoff=75. marks=95 => above = 20 (> 15).
        # low income => rate = 100 + 40 + 20 = 160.
        # expected = 20 * 160 = 3200
        assert award_amount("merit", 95, "low", False) == 3200

    def test_award_amount_high_marks_tier_non_low_income(self):
        # Branch: above > 15 -> True AND income_level != "low" (inner low check is False)
        # sports cutoff=60. marks=80 => above = 20 (> 15).
        # non-low income => rate = 60 + 40 = 100.
        # expected = 20 * 100 = 2000
        assert award_amount("sports", 80, "medium", False) == 2000

    def test_award_amount_normal_marks_tier_non_low_income(self):
        # Branch: above <= 15 (skips above > 15) AND income_level != "low"
        # arts cutoff=65. marks=75 => above = 10 (<= 15).
        # non-low income => rate = 60.
        # expected = 10 * 60 = 600
        assert award_amount("arts", 75, "high", False) == 600

    # =========================================================================
    # Function 2: is_eligible(attendance, backlogs, is_special_quota)
    # =========================================================================

    def test_is_eligible_special_quota_true_eligible(self):
        # Branch: is_special_quota=True -> evaluates backlogs <= 2 (True)
        assert is_eligible(50, 2, True) is True

    def test_is_eligible_special_quota_true_ineligible(self):
        # Branch: is_special_quota=True -> evaluates backlogs <= 2 (False)
        assert is_eligible(50, 3, True) is False

    def test_is_eligible_regular_quota_low_attendance(self):
        # Branch: is_special_quota=False -> attendance < 75 (True -> returns False)
        assert is_eligible(74, 0, False) is False

    def test_is_eligible_regular_quota_sufficient_attendance_pass(self):
        # Branch: is_special_quota=False -> attendance >= 75 (False) -> backlogs <= 1 (True)
        assert is_eligible(75, 1, False) is True

    def test_is_eligible_regular_quota_sufficient_attendance_fail(self):
        # Branch: is_special_quota=False -> attendance >= 75 (False) -> backlogs <= 1 (False)
        assert is_eligible(80, 2, False) is False

    # =========================================================================
    # Function 3: application_status(days_left, is_renewal, is_paper)
    # =========================================================================

    def test_application_status_renewal_paper_open(self):
        # Branch: is_renewal=True (cutoff=30), is_paper=True (cutoff=40)
        # days_left >= cutoff (40 >= 40 -> True => "open")
        assert application_status(40, True, True) == "open"

    def test_application_status_renewal_non_paper_open(self):
        # Branch: is_renewal=True (cutoff=30), is_paper=False (cutoff=30)
        # days_left >= cutoff (30 >= 30 -> True => "open")
        assert application_status(30, True, False) == "open"

    def test_application_status_non_renewal_paper_closing(self):
        # Branch: is_renewal=False (cutoff=20), is_paper=True (cutoff=30)
        # days_left < cutoff (25 < 30) AND days_left >= cutoff - 15 (25 >= 15 -> True => "closing")
        assert application_status(25, False, True) == "closing"

    def test_application_status_non_renewal_non_paper_closed(self):
        # Branch: is_renewal=False (cutoff=20), is_paper=False (cutoff=20)
        # days_left < cutoff - 15 (4 < 5 -> False => "closed")
        assert application_status(4, False, False) == "closed"

    def test_application_status_boundary_closing(self):
        # Exact boundary: cutoff=20 (renewal=False, paper=False), cutoff-15 = 5.
        # days_left=5 -> "closing"
        assert application_status(5, False, False) == "closing"

    def test_application_status_boundary_closed(self):
        # Exact boundary: days_left = cutoff - 16 = 4 -> "closed"
        assert application_status(4, False, False) == "closed"
