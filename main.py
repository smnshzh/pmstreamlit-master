import streamlit as st
import pandas as pd

# Sample data
projects_data = {
    "Project ID": [1, 2, 3],
    "Project Name": ["Project A", "Project B", "Project C"],
    "Status": ["Active", "Inactive", "Active"]
}

documents_data = {
    "Document ID": [1, 2],
    "Project ID": [1, 2],
    "Document Name": ["Doc A", "Doc B"]
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Projects", "Documents", "Reports", "Categories & Questionnaires"])

# Projects Page
if selection == "Projects":
    st.title("🏗️ Project Hub")
    st.subheader("View and manage your projects here.")
    
    # Display projects in a table
    projects_df = pd.DataFrame(projects_data)
    st.dataframe(projects_df)
    
    # Add new project
    st.sidebar.subheader("Create New Project")
    new_project_name = st.sidebar.text_input("Project Name")
    new_project_status = st.sidebar.selectbox("Status", ["Active", "Inactive"])
    
    if st.sidebar.button("Add Project"):
        new_id = len(projects_df) + 1
        new_project = pd.DataFrame({
            "Project ID": [new_id],
            "Project Name": [new_project_name],
            "Status": [new_project_status]
        })
        projects_df = pd.concat([projects_df, new_project], ignore_index=True)
        st.success(f"Project '{new_project_name}' added!")

# Documents Page
elif selection == "Documents":
    st.title("📄 Document Central")
    st.subheader("Manage your documents efficiently.")
    
    # Display documents based on selected projects
    selected_project = st.selectbox("Select Project", projects_df["Project Name"])
    filtered_docs = documents_data['Document ID']  # Placeholder for actual filtering logic
    st.write(f"Documents for {selected_project}: {filtered_docs}")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.success(f"Uploaded '{uploaded_file.name}' successfully!")

# Reports Page
elif selection == "Reports":
    st.title("📊 Report Generation")
    st.subheader("Create and manage reports.")
    
    # Step-by-step report creation
    report_title = st.text_input("Report Title")
    report_content = st.text_area("Report Content")
    
    if st.button("Generate Report"):
        st.success(f"Report '{report_title}' generated!")
        # Placeholder for exporting logic

# Categories & Questionnaires Page
elif selection == "Categories & Questionnaires":
    st.title("🏷️ Categories & Questionnaires")
    st.subheader("Manage categories and questionnaires.")
    
    # Interactive category management
    category_name = st.text_input("Category Name")
    if st.button("Add Category"):
        st.success(f"Category '{category_name}' added!")
    
    # Questionnaire creation
    questionnaire_title = st.text_input("Questionnaire Title")
    if st.button("Create Questionnaire"):
        st.success(f"Questionnaire '{questionnaire_title}' created!")

