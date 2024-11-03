import streamlit as st
import sqlite3
from database import get_connection, initialize_database

# Initialize the database
initialize_database()

st.title("Project Management App")

# Sidebar for navigation
menu = ["Add Project", "Add Task", "Assign Team Member", "View Projects"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Project":
    st.subheader("Create a New Project")

    with st.form("project_form"):
        project_name = st.text_input("Project Name")
        description = st.text_area("Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        submit_project = st.form_submit_button("Add Project")

    if submit_project:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (name, description, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """, (project_name, description, str(start_date), str(end_date)))
        conn.commit()
        conn.close()
        st.success(f"Project '{project_name}' added successfully.")

elif choice == "Add Task":
    st.subheader("Create a New Task")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()
    conn.close()

    project_options = {project[1]: project[0] for project in projects}

    with st.form("task_form"):
        project_name = st.selectbox("Select Project", list(project_options.keys()))
        task_name = st.text_input("Task Name")
        description = st.text_area("Description")
        submit_task = st.form_submit_button("Add Task")

    if submit_task:
        project_id = project_options[project_name]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (project_id, name, description)
            VALUES (?, ?, ?)
        """, (project_id, task_name, description))
        conn.commit()
        conn.close()
        st.success(f"Task '{task_name}' added to project '{project_name}' successfully.")

elif choice == "Assign Team Member":
    st.subheader("Assign Team Member to Task")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM tasks")
    tasks = cursor.fetchall()

    cursor.execute("SELECT id, name FROM team_members")
    members = cursor.fetchall()
    conn.close()

    task_options = {task[1]: task[0] for task in tasks}
    member_options = {member[1]: member[0] for member in members}

    with st.form("assignment_form"):
        task_name = st.selectbox("Select Task", list(task_options.keys()))
        member_name = st.selectbox("Select Team Member", list(member_options.keys()))
        submit_assignment = st.form_submit_button("Assign Member")

    if submit_assignment:
        task_id = task_options[task_name]
        member_id = member_options[member_name]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO task_assignments (task_id, member_id)
            VALUES (?, ?)
        """, (task_id, member_id))
        conn.commit()
        conn.close()
        st.success(f"Member '{member_name}' assigned to task '{task_name}' successfully.")

elif choice == "View Projects":
    st.subheader("Project Overview")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, start_date, end_date, status FROM projects
    """)
    projects = cursor.fetchall()
    conn.close()

    for project in projects:
        st.write(f"**{project[1]}**")
        st.write(f"Description: {project[2]}")
        st.write(f"Start Date: {project[3]}")
        st.write(f"End Date: {project[4]}")
        st.write(f"Status: {project[5]}")
        st.markdown("---")
