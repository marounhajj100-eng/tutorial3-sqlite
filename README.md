# Tutorial 3 – SQLite Exercise (Solution)

This repo contains a Python solution for the Tutorial 3 SQLite exercise:

- Create a database named `students` with **3 tables**: `student`, `registered_courses`, `grades`
- Insert sample data
- Query:
  - The **maximum grade** a student obtained with the **corresponding course_id** and student_id
  - The **average grade** of each student

## Run

```bash
python3 sqlite_tutorial3_solution.py
```

It will create `students.db` in the same folder, insert sample data, and print the query results.

## Notes

- Foreign keys are enabled with `PRAGMA foreign_keys = ON;`.
- `registered_courses` uses a **composite primary key** `(student_id, course_id)`.
- `grades` also uses `(student_id, course_id)` and enforces that this pair exists in `registered_courses`.
