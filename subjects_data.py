"""
subjects_data.py

Stores every IB subject available in the planner.
This keeps the project modular and makes future updates easier.
"""

IB_SUBJECTS = {

    "Group 1 - Studies in Language and Literature": [
        "English A Language & Literature",
        "English A Literature",
        "Portuguese A Language & Literature",
        "Spanish A Language & Literature",
        "Mandarin A Language & Literature",
        "French A Language & Literature",
    ],

    "Group 2 - Language Acquisition": [
        "English B",
        "French B",
        "German B",
        "Portuguese B",
        "Spanish B",
        "Mandarin B"
    ],

    "Group 3 - Individuals & Societies": [
        "Business Management",
        "Digital Society",
        "Economics",
        "Geography",
        "History",
        "Philosophy",
        "Psychology"
    ],

    "Group 4 - Sciences": [
        "Biology",
        "Chemistry",
        "Computer Science",
        "Design Technology",
        "Physics",
        "Environmental Systems & Societies"
    ],

    "Group 5 - Mathematics": [
        "Mathematics AA",
        "Mathematics AI"
    ],

    "Group 6 - Arts": [
        "Dance",
        "Film",
        "Music",
        "Theatre",
        "Visual Arts"
    ]

}
# ---------------------------------------
# Reverse Lookup Dictionary
# ---------------------------------------

SUBJECT_TO_GROUP = {}

for group, subjects in IB_SUBJECTS.items():
    for subject in subjects:
        SUBJECT_TO_GROUP[subject] = group