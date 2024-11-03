import streamlit as st
import sqlite3
from database import get_connection, initialize_database

# Initialize the database
initialize_database()

st.title("Project Management App")

# Sidebar for navigation
menu = ["Add Project", "Add Task", "Assign Team Member", "View Projects", "Edit Project"]
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

elif choice == "Edit Project":
    st.subheader("Edit an Existing Project")

    # Fetch all projects from the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()
    conn.close()

    project_options = {project[1]: project[0] for project in projects}

    if project_options:
        # Select project to edit
        project_name = st.selectbox("Select Project to Edit", list(project_options.keys()))
        project_id = project_options[project_name]

        # Fetch project details
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, start_date, end_date, status FROM projects WHERE id = ?", (project_id,))
        project_data = cursor.fetchone()
        conn.close()
        st.write(project_data)
        # Check if project_data exists before proceeding
        if project_data:
            # Convert start and end dates from string to datetime.date objects, handling None values
            if project_data[2] and project_data[3]:
                start_date = datetime.strptime(project_data[3], "%Y-%m-%d").date() if project_data[2] else date.today()
                end_date = datetime.strptime(project_data[3], "%Y-%m-%d").date() if project_data[3] else date.today()

            # Pre-fill form with existing project data
            with st.form("edit_project_form"):
                new_project_name = st.text_input("Project Name", value=project_data[0])
                new_description = st.text_area("Description", value=project_data[1])
                new_start_date = st.date_input("Start Date", value=start_date)
                new_end_date = st.date_input("End Date", value=end_date)
                new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(project_data[4]))

                submit_edit = st.form_submit_button("Update Project")

            if submit_edit:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE projects
                    SET name = ?, description = ?, start_date = ?, end_date = ?, status = ?
                    WHERE id = ?
                """, (new_project_name, new_description, str(new_start_date), str(new_end_date), new_status, project_id))
                conn.commit()
                conn.close()
                st.success(f"Project '{new_project_name}' updated successfully.")
        else:
            st.error("Could not find project details. Please try another project.")
    else:
        st.warning("No projects found. Please add a project first.")

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
