import math

def parse_applicant(text):
    if not isinstance(text, str) or text is None:
        return None
    if ':' not in text:
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    category = parts[0].strip()
    if not category:
        return None
    try:
        marks = float(parts[1].strip())
        if math.isnan(marks) or math.isinf(marks):
            return None
        return category.title(), marks
    except (ValueError, TypeError):
        return None


def marks_average(marks_csv):
    if not isinstance(marks_csv, str) or marks_csv is None:
        return None
    parts = [r.strip() for r in marks_csv.split(',')]
    if not parts or any(r == '' for r in parts):
        return None
    try:
        values = [int(r) for r in parts]
        if not values:
            return None
        return sum(values) // len(values)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def payable_award(text):
    if not isinstance(text, str) or text is None:
        return None
    if '|' not in text:
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        award = float(parts[0].strip())
        deduction = float(parts[1].strip())
        if math.isnan(award) or math.isinf(award) or math.isnan(deduction) or math.isinf(deduction):
            return None
        total = award * 1.18 - deduction
        return max(total, 0.0)
    except (ValueError, TypeError):
        return None


def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    result = parse_applicant(user_input)
    print("Category and Marks:", result)

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    result = marks_average(user_input)
    print("Average Marks:", result)

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    result = payable_award(user_input)
    print("Payable Award:", result)


if __name__ == "__main__":
    main()

