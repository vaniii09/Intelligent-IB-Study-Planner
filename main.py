from database import create_tables
from database import populate_default_subjects
from database import get_subjects


# Create database tables
create_tables()


# Insert default subjects (only once)
populate_default_subjects()


# Display all subjects

print("\nSubjects in Database\n")

subjects = get_subjects()

for subject in subjects:
    print(subject)