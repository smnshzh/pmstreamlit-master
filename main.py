import streamlit as st
import subprocess

# Title of the app
st.title("Linux Command Executor")

# Input for the command
command = st.text_input("Enter a Linux command:", "ls")

# Button to execute the command
if st.button("Execute"):
    try:
        # Execute the command and get the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Display the output
        if result.returncode == 0:
            st.success("Command executed successfully!")
            st.text(result.stdout)
        else:
            st.error("Error executing command:")
            st.text(result.stderr)
    except Exception as e:
        st.error(f"An error occurred: {e}")
