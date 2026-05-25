import streamlit as st
import requests
import pandas as pd 

server_location = "http://127.0.0.1:8000"

st.title("Student Management Portal")

opt = st.sidebar.selectbox("Select an option", ["Add Student", "View Students", "Update Student", "Delete Student" ])

if opt == "Add Student":
    st.header("Add a new student")
    with st.form("add_student_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        grade = st.text_input("Grade")
        section = st.text_input("Section")
        Father_name = st.text_input("father_Name")
        Village = st.text_input("village")
        submit_button = st.form_submit_button("Add Student")

    if submit_button:
        student_data = {
            "name": name,
            "age": age,
            "grade": grade,
            "section": section,
            "father_name": Father_name,
            "village": Village
        }
        response = requests.post(f"{server_location}/students", json=student_data)
        if response.status_code == 200:
            st.write(response.json())
            st.success("Student added successfully!")
        else:
            st.error("Failed to add student. Please try again.")


elif opt == "View Students":
    st.header("view all Students")
    if st.button("Get Students"):
        response = requests.get(f"{server_location}/get_students")
        students_data = response.json()
        a=students_data["students"]
        pd_df=pd.DataFrame(a)
        st.dataframe(pd_df)

elif opt == "Update Student":
    st.header("Update Student")
    student_id = st.number_input("Enter Student ID to Update", min_value=1)
    if st.button("fetch Student Data"):
        response = requests.get(f"{server_location}/get_single_student/{student_id}")
        st.write(response.json())
        if response.status_code == 200:
            st.session_state.name = response.json()["student_data"]["name"]
            st.session_state.age = response.json()["student_data"]["age"]
            st.session_state.grade = response.json()["student_data"]["grade"]
            st.session_state.section = response.json()["student_data"]["section"]       
            st.session_state.father_name = response.json()["student_data"]["father_name"]
            st.session_state.village = response.json()["student_data"]["village"]


    
    name = st.text_input("Name", value=st.session_state.name)
    age = st.number_input("Age", min_value=0, value=st.session_state.age)
    grade = st.text_input("Grade", value=st.session_state.grade)
    section = st.text_input("Section", value=st.session_state.section)
    Father_name = st.text_input("father_Name", value=st.session_state.father_name)
    Village = st.text_input("village", value=st.session_state.village)

    if st.button("Update Student"):
        updated_student_data = {
            "name": name,
            "age": age,
            "grade": grade,
            "section": section,
            "father_name": Father_name,
            "village": Village
        }   

        response = requests.put(f"{server_location}/update_student/{student_id}", json=updated_student_data)
        if response.status_code == 200:
            st.write(response.json())
            st.success("Student updated successfully!")


elif opt == "Delete Student":
    st.header("Delete Student")
    response = requests.get(f"{server_location}/get_students")
    students_data = response.json()
    a=students_data["students"]
    pd_df=pd.DataFrame(a)

    student_id_to_delete = st.number_input("Enter Student ID to Delete", min_value=1)

    if st.button("Delete Student"):
        response = requests.delete(f"{server_location}/delete_student/{student_id_to_delete}")
        if response.status_code == 200:
            st.write(response.json())
            st.success("Student deleted successfully!")
        else:
            st.error("Failed to delete student. Please try again.")