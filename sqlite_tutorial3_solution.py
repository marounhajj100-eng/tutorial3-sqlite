import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("students.db")


def print_rows(title: str, columns: list[str], rows: list[tuple]):
    print(f"\n{title}")
    print(" | ".join(columns))
    print("-" * max(30, len(" | ".join(columns))))
    for r in rows:
        print(" | ".join(str(x) for x in r))


def setup_database(conn: sqlite3.Connection) -> None:
    """Create the required tables (student, registered_courses, grades)."""
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()


    cur.execute("DROP TABLE IF EXISTS grades")
    cur.execute("DROP TABLE IF EXISTS registered_courses")
    cur.execute("DROP TABLE IF EXISTS student")

    cur.execute(
        """
        CREATE TABLE student (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """
    )

  
    cur.execute(
        """
        CREATE TABLE registered_courses (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES student(student_id)
        )
        """
    )

    
    cur.execute(
        """
        CREATE TABLE grades (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            grade REAL NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES student(student_id),
            FOREIGN KEY (student_id, course_id) REFERENCES registered_courses(student_id, course_id)
        )
        """
    )

    conn.commit()


def insert_sample_data(conn: sqlite3.Connection) -> None:
    """Insert at least 3 students, 3 courses (as IDs), and some grades."""
    cur = conn.cursor()

    students = [
        (1, "Alice", 20),
        (2, "Bob", 22),
        (3, "Charlie", 21),
    ]
    cur.executemany("INSERT INTO student(student_id, name, age) VALUES (?, ?, ?)", students)

    
    courses = [101, 102, 103]

    registered = [
        (1, 101),
        (1, 102),
        (2, 101),
        (2, 103),
        (3, 102),
        (3, 103),
    ]
    cur.executemany("INSERT INTO registered_courses(student_id, course_id) VALUES (?, ?)", registered)

    grades = [
        (1, 101, 88.5),
        (1, 102, 92.0),
        (2, 101, 76.0),
        (2, 103, 90.0),
        (3, 102, 90.0),
        (3, 103, 90.0), 
    ]
    cur.executemany("INSERT INTO grades(student_id, course_id, grade) VALUES (?, ?, ?)", grades)

    conn.commit()


def query_max_grade_with_course(conn: sqlite3.Connection) -> list[tuple]:
    """Return (student_id, course_id, max_grade) for each student.

    If a student has multiple courses tied for max grade, all tied rows are returned.
    """
    cur = conn.cursor()
    cur.execute(
        """
        WITH max_per_student AS (
            SELECT student_id, MAX(grade) AS max_grade
            FROM grades
            GROUP BY student_id
        )
        SELECT g.student_id, g.course_id, g.grade AS max_grade
        FROM grades g
        JOIN max_per_student m
          ON g.student_id = m.student_id
         AND g.grade = m.max_grade
        ORDER BY g.student_id, g.course_id;
        """
    )
    return cur.fetchall()


def query_avg_grade_per_student(conn: sqlite3.Connection) -> list[tuple]:
    """Return (student_id, avg_grade) for each student."""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT student_id, ROUND(AVG(grade), 2) AS avg_grade
        FROM grades
        GROUP BY student_id
        ORDER BY student_id;
        """
    )
    return cur.fetchall()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)

    try:
        setup_database(conn)
        insert_sample_data(conn)

        
        cur = conn.cursor()
        for t in ("student", "registered_courses", "grades"):
            cur.execute(f"SELECT * FROM {t}")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            print_rows(f"Table: {t}", cols, rows)

        
        max_rows = query_max_grade_with_course(conn)
        print_rows(
            "Max grade per student (with corresponding course_id)",
            ["student_id", "course_id", "max_grade"],
            max_rows,
        )

        avg_rows = query_avg_grade_per_student(conn)
        print_rows(
            "Average grade per student",
            ["student_id", "avg_grade"],
            avg_rows,
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
