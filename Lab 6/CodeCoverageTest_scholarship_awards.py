import pytest
from scholarship_awards import award_amount, is_eligible, application_status


class TestCodeCoverageScholarshipAwards:
    # ---------------- award_amount tests ----------------
    def test_award_amount_unknown_category_raises_error(self):
        with pytest.raises(ValueError, match="unknown category"):
            award_amount("dance", 80, "low", False)

    def test_award_amount_negative_marks_raises_error(self):
        with pytest.raises(ValueError, match="invalid marks"):
            award_amount("merit", -5, "low", False)

    def test_award_amount_below_cutoff(self):
        # merit cutoff=75, marks=70 => above = -5 <= 0 => returns 0
        assert award_amount("merit", 70, "low", False) == 0

    def test_award_amount_renewal_non_sports_low_income_high_marks(self):
        # merit renewal => cutoff = 75 - 5 = 70.
        # marks=90 => above = 20 (> 15).
        # low income => rate = 100 + 40 + 20 = 160.
        # total = 20 * 160 = 3200
        assert award_amount("merit", 90, "low", True) == 3200

    def test_award_amount_non_low_income_high_marks(self):
        # sports non-renewal => cutoff=60. marks=80 => above = 20 (> 15).
        # non-low income => rate = 60 + 40 = 100.
        # total = 20 * 100 = 2000
        assert award_amount("sports", 80, "medium", False) == 2000

    # ---------------- is_eligible tests ----------------
    def test_is_eligible_special_quota(self):
        assert is_eligible(60, 2, True) is True

    def test_is_eligible_low_attendance(self):
        assert is_eligible(70, 0, False) is False

    def test_is_eligible_regular_quota_passes(self):
        assert is_eligible(85, 1, False) is True

    # ---------------- application_status tests ----------------
    def test_application_status_renewal_paper_open(self):
        # is_renewal=True (cutoff=30), is_paper=True (cutoff=40). days_left=45 >= 40 => "open"
        assert application_status(45, True, True) == "open"

    def test_application_status_closing(self):
        # is_renewal=False (cutoff=20), is_paper=False (cutoff=20).
        # days_left=10 (>= 20 - 15 = 5) => "closing"
        assert application_status(10, False, False) == "closing"

    def test_application_status_closed(self):
        # is_renewal=False (cutoff=20), is_paper=False (cutoff=20).
        # days_left=2 (< 5) => "closed"
        assert application_status(2, False, False) == "closed"
