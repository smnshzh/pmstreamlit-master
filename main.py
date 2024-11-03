import streamlit as st
import sqlite3
from database import get_connection, initialize_database
from datetime import datetime, date

# Initialize the database
initialize_database()

st.title("Project Management App")

# Sidebar for navigation
menu = ["Add Project", "Add Task", "Assign Team Member", "View Projects", "Edit Project", "Add Team", "Add Member"]
choice = st.sidebar.selectbox("Menu", menu)

# Function to add a new project
if choice == "Add Project":
    st.subheader("Add a New Project")

    with st.form("add_project_form"):
        project_name = st.text_input("Project Name")
        description = st.text_area("Description")
        start_date = st.date_input("Start Date", value=date.today())
        end_date = st.date_input("End Date", value=date.today())
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])

        submit_add = st.form_submit_button("Add Project")

    if submit_add:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
        duplicate_project = cursor.fetchone()

        if duplicate_project:
            st.error("A project with this name already exists. Please choose a different name.")
        else:
            cursor.execute("""INSERT INTO projects (name, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)""",
                           (project_name, description, str(start_date), str(end_date), status))
            conn.commit()
            conn.close()
            st.success(f"Project '{project_name}' added successfully.")

# Function to edit an existing project
elif choice == "Edit Project":
    st.subheader("Edit or Delete an Existing Project")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()
    conn.close()

    project_options = {project[1]: project[0] for project in projects}

    if project_options:
        project_name = st.selectbox("Select Project to Edit or Delete", list(project_options.keys()))
        project_id = project_options[project_name]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, start_date, end_date, status FROM projects WHERE id = ?", (project_id,))
        project_data = cursor.fetchone()
        conn.close()

        if project_data:
            start_date = datetime.strptime(project_data[2], "%Y-%m-%d").date() if project_data[2] else date.today()
            end_date = datetime.strptime(project_data[3], "%Y-%m-%d").date() if project_data[3] else date.today()

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
                cursor.execute("SELECT id FROM projects WHERE name = ? AND id != ?", (new_project_name, project_id))
                duplicate_project = cursor.fetchone()

                if duplicate_project:
                    st.error("A project with this name already exists. Please choose a different name.")
                else:
                    cursor.execute("""UPDATE projects SET name = ?, description = ?, start_date = ?, end_date = ?, status = ? WHERE id = ?""",
                                   (new_project_name, new_description, str(new_start_date), str(new_end_date), new_status, project_id))
                    conn.commit()
                    conn.close()
                    st.success(f"Project '{new_project_name}' updated successfully.")

            delete_confirm = st.button("Delete Project")
            if delete_confirm:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
                conn.commit()
                conn.close()
                st.success(f"Project '{project_name}' deleted successfully.")
    else:
        st.warning("No projects found. Please add a project first.")

# Function to add a new task
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
        cursor.execute("""INSERT INTO tasks (project_id, name, description) VALUES (?, ?, ?)""", (project_id, task_name, description))
        conn.commit()
        conn.close()
        st.success(f"Task '{task_name}' added to project '{project_name}' successfully.")

# Function to assign a team member to a task
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
        cursor.execute("""INSERT INTO task_assignments (task_id, member_id) VALUES (?, ?)""", (task_id, member_id))
        conn.commit()
        conn.close()
        st.success(f"Member '{member_name}' assigned to task '{task_name}' successfully.")

# Function to view projects
elif choice == "View Projects":
    st.subheader("Project Overview")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT id, name, description, start_date, end_date, status FROM projects""")
    projects = cursor.fetchall()
    conn.close()

    for project in projects:
        st.write(f"**{project[1]}**")
        st.write(f"Description: {project[2]}")
        st.write(f"Start Date: {project[3]}")
        st.write(f"End Date: {project[4]}")
        st.write(f"Status: {project[5]}")
        st.markdown("---")

# Function to add a new team
elif choice == "Add Team":
    st.subheader("Add a New Team")

    with st.form("add_team_form"):
        team_name = st.text_input("Team Name")
        team_description = st.text_area("Team Description")
        submit_team = st.form_submit_button("Add Team")

    if submit_team:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO teams (name, description) VALUES (?, ?)", (team_name, team_description))
        conn.commit()
        conn.close()
        st.success(f"Team '{team_name}' added successfully.")

# Function to add a new team member
elif choice == "Add Member":
    st.subheader("Add a New Team Member")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()
    conn.close()

    team_options = {team[1]: team[0] for team in teams}

    with st.form("add_member_form"):
        member_name = st.text_input("Member Name")
        selected_team = st.selectbox("Select Team", list(team_options.keys()))
        submit_member = st.form_submit_button("Add Member")

    if submit_member:
        team_id = team_options[selected_team]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO team_members (name, team_id) VALUES (?, ?)", (member_name, team_id))
        conn.commit()
        conn.close()
        st.success(f"Member '{member_name}' added to team '{selected_team}' successfully.")
