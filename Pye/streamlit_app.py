"""
COS201 Student Course Management System - Streamlit web version.
Reuses the CourseManager class from course_manager.py unchanged.
Run locally with:  streamlit run streamlit_app.py
"""

import csv
import os
import tempfile

import streamlit as st

from course_manager import CourseManager, InvalidCourseError

st.set_page_config(page_title="Student Course Management", page_icon="📚")
st.title("📚 Student Course Management System")

# Streamlit reruns this script on every click, so the manager lives in session_state.
if "manager" not in st.session_state:
    st.session_state.manager = CourseManager()
manager = st.session_state.manager

OPTIONS = [
    "1. Add Course",
    "2. View All Courses",
    "3. Search Course by Code",
    "4. Compute Total Units",
    "5. Save to File",
    "6. Load from File",
    "7. Exit Program",
]
choice = st.sidebar.radio("Menu", OPTIONS)

if choice == OPTIONS[0]:
    st.subheader("Add Course")
    with st.form("add_form", clear_on_submit=True):
        code = st.text_input("Course code (e.g. COS201)")
        title = st.text_input("Course title")
        units = st.text_input("Credit units")
        submitted = st.form_submit_button("Add course")
    if submitted:
        try:
            saved = manager.add_course(code, title, units)
            st.success(f"Course {saved} added successfully.")
        except InvalidCourseError as err:
            st.error(str(err))

elif choice == OPTIONS[1]:
    st.subheader("All Courses")
    if not manager.courses:
        st.info("No courses recorded yet.")
    else:
        st.table(
            [{"Code": c.code, "Title": c.title, "Units": c.units} for c in manager.courses]
        )

elif choice == OPTIONS[2]:
    st.subheader("Search Course by Code")
    query = st.text_input("Enter course code")
    if st.button("Search"):
        course = manager.find_course(query)
        if course:
            st.success("Course found")
            st.table([{"Code": course.code, "Title": course.title, "Units": course.units}])
        else:
            st.warning("No course found with that code.")

elif choice == OPTIONS[3]:
    st.subheader("Total Units")
    st.metric("Total credit units", manager.total_units())

elif choice == OPTIONS[4]:
    st.subheader("Save to File")
    if not manager.courses:
        st.info("Nothing to save yet. Add some courses first.")
    else:
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            manager.save_to_file(path)
            with open(path, "rb") as f:
                data = f.read()
        finally:
            os.remove(path)
        st.download_button("Download courses.csv", data, "courses.csv", "text/csv")

elif choice == OPTIONS[5]:
    st.subheader("Load from File")
    uploaded = st.file_uploader("Choose a courses.csv file", type="csv")
    if st.button("Load courses") and uploaded is not None:
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            with open(path, "wb") as f:
                f.write(uploaded.getvalue())
            count = manager.load_from_file(path)
            st.success(f"Loaded {count} course(s).")
        except (InvalidCourseError, IOError, UnicodeDecodeError, csv.Error) as err:
            st.error(f"Could not load file: {err}")
        finally:
            os.remove(path)
    elif uploaded is None:
        st.caption("Upload a file first, then click Load courses.")

else:
    st.subheader("Exit Program")
    st.write("Goodbye! You can close this browser tab.")
