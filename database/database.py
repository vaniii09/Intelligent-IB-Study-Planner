from asyncio import tasks
import sqlite3
from datetime import datetime, timedelta

DATABASE_NAME = "database/planner.db"

def get_connection():
    """
    Creates and returns a connection to the database.
    """
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    """
    Creates every table required by the planner.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # Subjects
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects(

        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        level TEXT NOT NULL
    )
    """)

    # -------------------------
    # Availability
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Availability(

        day TEXT PRIMARY KEY,

        hours INTEGER NOT NULL
    )
    """)

    # -------------------------
    # Tasks
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tasks(

        task_id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        subject TEXT NOT NULL,

        task_type TEXT NOT NULL,

        deadline TEXT NOT NULL,

        estimated_hours REAL NOT NULL,

        priority REAL DEFAULT 0,

        completed INTEGER DEFAULT 0
    )
    """)
    # -------------------------
    # Database Migration
    # -------------------------

    try:
        cursor.execute("""
            ALTER TABLE Tasks
            ADD COLUMN completed_date TEXT
        """)
    except:
        pass

    try:
        cursor.execute("""
            ALTER TABLE Tasks
            ADD COLUMN archived INTEGER DEFAULT 0
        """)
    except:
        pass
    connection.commit()
    connection.close()


def save_subjects(subjects, levels):
    """
    Saves the user's chosen subjects.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Subjects")

    for subject in subjects:
        cursor.execute(
            """
            INSERT INTO Subjects(name, level)
            VALUES (?, ?)
            """,
            (
                subject,
                levels[subject]
            )
        )

    connection.commit()
    connection.close()


def save_availability(availability):
    """
    Saves study hours for each day.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Availability")

    for day, hours in availability.items():
        cursor.execute(
            """
            INSERT INTO Availability(day, hours)
            VALUES (?, ?)
            """,
            (
                day,
                int(hours.get())
            )
        )

    connection.commit()
    connection.close()


def load_subjects():
    """
    Returns every saved subject.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, level
        FROM Subjects
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def get_subject_level(subject):
    """
    Returns the HL/SL level for a subject.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT level
        FROM Subjects
        WHERE name = ?
        """,
        (subject,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return "SL"

def load_availability():
    """
    Returns all saved availability.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT day, hours
        FROM Availability
    """)

    data = cursor.fetchall()

    connection.close()

    return data

def save_task(title, subject, task_type, deadline, hours, priority):
    """
    Saves a task to the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO Tasks
        (
            title,
            subject,
            task_type,
            deadline,
            estimated_hours,
            priority
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            subject,
            task_type,
            deadline,
            float(hours),
            priority
        )
    )

    connection.commit()
    connection.close()

def load_tasks():
    """
    Returns every task saved in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            task_id,
            title,
            subject,
            task_type,
            deadline,
            estimated_hours,
            priority,
            completed,
            completed_date,
            archived
        FROM Tasks
        ORDER BY deadline
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks

def get_task(task_id):
    """
    Returns one task from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            task_id,
            title,
            subject,
            task_type,
            deadline,
            estimated_hours,
            priority,
            completed,
            completed_date,
            archived
        FROM Tasks
        WHERE task_id = ?
        """,
        (task_id,)
    )

    task = cursor.fetchone()

    connection.close()

    return task

def get_dashboard_statistics():
    """
    Returns dashboard statistics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Tasks"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Tasks
        WHERE completed = 1
        """
    )
    completed = cursor.fetchone()[0]

    pending = total - completed

    cursor.execute(
        """
        SELECT title, priority
        FROM Tasks
        WHERE completed = 0
        ORDER BY priority DESC
        LIMIT 1
        """
    )

    highest = cursor.fetchone()

    if total == 0:
        progress = 0
    else:
        progress = (completed / total) * 100

    connection.close()

    return (
        total,
        completed,
        pending,
        highest,
        progress
    )

def delete_task(task_id):
    """
    Deletes a task from the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM Tasks
        WHERE task_id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()

def mark_task_complete(task_id):
    """
    Marks a task as completed.
    """

    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
        UPDATE Tasks
        SET
            completed = 1,
            completed_date = ?
        WHERE task_id = ?
        """,
        (today, task_id)
    )

    connection.commit()
    connection.close()

def has_completed_setup():
    """
    Returns True if the user has already completed setup.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM Subjects
        """
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count > 0

def update_task(
    task_id,
    title,
    subject,
    task_type,
    deadline,
    estimated_hours,
    priority
):
    """
    Updates an existing task.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Tasks
        SET
            title = ?,
            subject = ?,
            task_type = ?,
            deadline = ?,
            estimated_hours = ?,
            priority = ?
        WHERE task_id = ?
        """,
        (
            title,
            subject,
            task_type,
            deadline,
            estimated_hours,
            priority,
            task_id
        )
    )

    connection.commit()
    connection.close()

def update_subject_level(subject, level):
    """
    Updates a subject's HL/SL level.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Subjects
        SET level = ?
        WHERE name = ?
        """,
        (
            level,
            subject
        )
    )

    connection.commit()
    connection.close()


def update_availability(day, hours):
    """
    Updates the available study hours for a day.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Availability
        SET hours = ?
        WHERE day = ?
        """,
        (
            int(hours),
            day
        )
    )

    connection.commit()
    connection.close() 

def search_tasks(search="", subject="All", status="All", sort="Priority"):

    tasks = load_tasks()

    # --------------------------------------------------
    # Remove archived tasks unless requested
    # --------------------------------------------------

    if status != "Archived":

        tasks = [
            task for task in tasks
            if not task[9]
        ]

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    if search:

        tasks = [
            task for task in tasks
            if search.lower() in task[1].lower()
        ]

    # --------------------------------------------------
    # Subject Filter
    # --------------------------------------------------

    if subject != "All":

        tasks = [
            task for task in tasks
            if task[2] == subject
        ]

    # --------------------------------------------------
    # Status Filter
    # --------------------------------------------------

    if status == "Completed":

        tasks = [
            task for task in tasks
            if task[7] and not task[9]
        ]

    elif status == "Pending":

        tasks = [
            task for task in tasks
            if not task[7] and not task[9]
        ]

    elif status == "Archived":

        tasks = [
            task for task in tasks
            if task[9]
        ]

    # --------------------------------------------------
    # Sorting
    # --------------------------------------------------

    if sort == "Priority":

        tasks.sort(
            key=lambda x: x[6] if x[6] else 0,
            reverse=True
        )

    elif sort == "Deadline":

        tasks.sort(
            key=lambda x: x[4]
        )

    elif sort == "Title":

        tasks.sort(
            key=lambda x: x[1]
        )

    elif sort == "Subject":

        tasks.sort(
            key=lambda x: x[2]
        )

    return tasks
def archive_old_tasks():
    """
    Moves completed tasks older than 7 days to the archive.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cutoff = (
        datetime.now() - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    cursor.execute(
        """
        UPDATE Tasks
        SET archived = 1
        WHERE
            completed = 1
            AND archived = 0
            AND completed_date IS NOT NULL
            AND completed_date <= ?
        """,
        (cutoff,)
    )

    connection.commit()
    connection.close()