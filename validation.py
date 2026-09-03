from subjects_data import SUBJECT_TO_GROUP


def validate_subject_selection(wizard):
    """
    Validates the IB subject combination.
    """

    subjects = wizard.selected_subjects
    levels = wizard.selected_levels

    group_count = {}

    for subject in subjects:
        group = SUBJECT_TO_GROUP[subject]
        group_count[group] = group_count.get(group, 0) + 1

    # ----------------------------
    # Exactly 6 subjects
    # ----------------------------

    if len(subjects) != 6:
        return False, (
            f"You have selected {len(subjects)} subjects.\n\n"
            "Please select exactly 6 subjects."
        )

    # ----------------------------
    # Count HL subjects
    # ----------------------------

    hl_count = sum(
        1
        for level in levels.values()
        if level == "HL"
    )

    if hl_count < 3:
        return False, (
            "You must select at least 3 Higher Level (HL) subjects."
        )

    if hl_count > 4:
        return False, (
            "You may select at most 4 Higher Level (HL) subjects."
        )

    # ----------------------------
    # Required groups
    # ----------------------------

    required_groups = [
        "Group 1 - Studies in Language and Literature",
        "Group 2 - Language Acquisition",
        "Group 4 - Sciences",
        "Group 5 - Mathematics"
    ]

    for group in required_groups:
        if group_count.get(group, 0) == 0:
            return False, (
                f"You must choose at least one subject from\n\n{group}"
            )

    # ----------------------------
    # Group 3 / Group 6 Rule
    # ----------------------------

    group1 = group_count.get(
        "Group 1 - Studies in Language and Literature", 0
    )

    group2 = group_count.get(
        "Group 2 - Language Acquisition", 0
    )

    group3 = group_count.get(
        "Group 3 - Individuals & Societies", 0
    )

    group4 = group_count.get(
        "Group 4 - Sciences", 0
    )

    group5 = group_count.get(
        "Group 5 - Mathematics", 0
    )

    group6 = group_count.get(
        "Group 6 - Arts", 0
    )

    # ----------------------------
    # IB Subject Combination Rules
    # ----------------------------

    # Must always have:
    # Group 1
    # Group 2
    # Group 5

    if group1 != 1:
        return False, "Choose exactly one Group 1 subject."

    if group2 < 1:
        return False, "Choose at least one Group 2 subject."

    if group5 != 1:
        return False, "Choose exactly one Mathematics subject."

    # Group 3 / 4 / 6 combinations

    standard_ib = (
        group3 == 1 and
        group4 == 1 and
        group6 == 1
    )

    extra_science = (
        group3 == 1 and
        group4 == 2 and
        group6 == 0
    )

    extra_humanity = (
        group3 == 2 and
        group4 == 1 and
        group6 == 0
    )

    three_sciences = (
        group3 == 0 and
        group4 == 3 and
        group6 == 0
    )

    if not (
        standard_ib or
        extra_science or
        extra_humanity or
        three_sciences
    ):
        return False, (
            "Invalid IB subject combination.\n\n"
            "Choose either:\n"
            "• Standard Diploma\n"
            "• Extra Science\n"
            "• Extra Humanities\n"
            "• Three Sciences"
        )
    # ----------------------------
    # Everything is valid
    # ----------------------------

    return True, ""