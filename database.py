import sqlite3

def get_connection():
    return sqlite3.connect("projects.db")

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'Not Started'
        )
    """)

    # Create Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)

    # Create Team Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    # Create Task Assignments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            member_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES tasks (id),
            FOREIGN KEY (member_id) REFERENCES team_members (id)
        )
    """)

    conn.commit()
    conn.close()
