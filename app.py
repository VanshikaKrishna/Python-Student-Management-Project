from abc import ABC, abstractmethod
import json
from pathlib import Path
import streamlit as st

# Set up page configuration
st.set_page_config(page_title="School Management System", page_icon="🎓", layout="centered")

# Initialize database
database = "school_data.json"
if "data" not in st.session_state:
    if Path(database).exists():
        with open(database, "r") as f:
            content = f.read()
            st.session_state.data = json.loads(content) if content else {"students": [], "teachers": []}
    else:
        st.session_state.data = {"students": [], "teachers": []}


def save():
    with open(database, "w") as f:
        json.dump(st.session_state.data, f, indent=4)


# Abstract Base Class
class Persons(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email


class Student(Persons):
    def get_roles(self):
        return "Student"

    def register(self, name, age, email, roll_no):
        if not Persons.validate_email(email):
            return "error", "Invalid Email Address"

        for i in st.session_state.data["students"]:
            if i["roll_no"] == roll_no:
                return "error", "Student already exists with this Roll Number"

        st.session_state.data["students"].append(
            {"name": name, "age": age, "email": email, "roll_no": roll_no, "grades": {}}
        )
        save()
        return "success", f"Student {name} registered successfully!"

    def add_grade(self, roll_no, subject, marks):
        for i in st.session_state.data["students"]:
            if i["roll_no"] == roll_no:
                if "grades" not in i:
                    i["grades"] = {}
                i["grades"][subject] = marks
                save()
                return "success", f"Grade added for {subject} successfully!"
        return "error", "Student not found"


class Teacher(Persons):
    def get_roles(self):
        return "Teacher"

    def register(self, name, age, email, subject, emp_id):
        if not Persons.validate_email(email):
            return "error", "Invalid Email Address"

        for i in st.session_state.data["teachers"]:
            if i["emp_id"] == emp_id:
                return "error", "Teacher already exists with this Employee ID"

        st.session_state.data["teachers"].append(
            {"name": name, "age": age, "email": email, "subject": subject, "emp_id": emp_id}
        )
        save()
        return "success", f"Teacher {name} registered successfully!"


# Instantiate core logic objects
stud = Student()
tech = Teacher()

# --- UI HEADER ---
st.title("🎓 School Management Dashboard")
st.markdown("---")

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("🧭 Navigation")
choice = st.sidebar.radio(
    "Choose an Action:",
    [
        "View Dashboard",
        "Register Student",
        "Register Teacher",
        "Add Student Grades",
        "Search Student Details",
        "Search Teacher Details",
    ],
)

# --- VIEW DASHBOARD ---
if choice == "View Dashboard":
    st.subheader("🏫 School Overview")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Students Registered", value=len(st.session_state.data["students"]))
    with col2:
        st.metric(label="Total Teachers Registered", value=len(st.session_state.data["teachers"]))

    st.markdown("### Quick Records View")
    tab1, tab2 = st.tabs(["Students", "Teachers"])

    with tab1:
        if st.session_state.data["students"]:
            st.dataframe(st.session_state.data["students"], use_container_width=True)
        else:
            st.info("No student records found.")

    with tab2:
        if st.session_state.data["teachers"]:
            st.dataframe(st.session_state.data["teachers"], use_container_width=True)
        else:
            st.info("No teacher records found.")

# --- REGISTER STUDENT ---
elif choice == "Register Student":
    st.subheader("📝 Student Registration Form")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=4, max_value=100, step=1)
        email = st.text_input("Email Address")
        roll_no = st.text_input("Roll Number")

        submitted = st.form_submit_button("Register Student")
        if submitted:
            if name and email and roll_no:
                status, msg = stud.register(name, age, email, roll_no)
                if status == "success":
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please fill out all fields.")

# --- REGISTER TEACHER ---
elif choice == "Register Teacher":
    st.subheader("📝 Teacher Registration Form")
    with st.form("teacher_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=20, max_value=100, step=1)
        email = st.text_input("Email Address")
        subject = st.text_input("Specialist Subject")
        emp_id = st.text_input("Employee ID")

        submitted = st.form_submit_button("Register Teacher")
        if submitted:
            if name and email and subject and emp_id:
                status, msg = tech.register(name, age, email, subject, emp_id)
                if status == "success":
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please fill out all fields.")

# --- ADD STUDENT GRADES ---
elif choice == "Add Student Grades":
    st.subheader("📊 Assign Grades")

    # Dynamic dropdown containing valid roll numbers
    student_list = [f"{s['roll_no']} - {s['name']}" for s in st.session_state.data["students"]]

    if not student_list:
        st.info("Please register a student first to add grades.")
    else:
        selected_student = st.selectbox("Select Student Profile", student_list)
        roll_no = selected_student.split(" - ")[0]

        with st.form("grades_form", clear_on_submit=True):
            subject = st.text_input("Subject Name")
            marks = st.number_input("Marks obtained", min_value=0.0, max_value=100.0, step=0.5)

            submitted = st.form_submit_button("Submit Grade")
            if submitted:
                if subject:
                    status, msg = stud.add_grade(roll_no, subject, marks)
                    if status == "success":
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Subject name cannot be blank.")

# --- SEARCH STUDENT DETAILS ---
elif choice == "Search Student Details":
    st.subheader("🔍 Look Up Student Profile")
    search_roll = st.text_input("Enter Roll Number to Search")

    if search_roll:
        found = False
        for s in st.session_state.data["students"]:
            if s["roll_no"] == search_roll:
                found = True
                grades = s["grades"]
                avg = sum(grades.values()) / len(grades) if grades else 0

                # Elegant visual layout for metrics
                st.success(f"Record found for {s['name']}!")

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {s['name']}")
                    st.write(f"**Roll Number:** {s['roll_no']}")
                    st.write(f"**Email:** {s['email']}")
                    st.write(f"**Age:** {s['age']}")
                with col2:
                    st.metric(label="Grade Average", value=f"{avg:.2f}")

                st.markdown("#### Subject Grades Breakdown")
                if grades:
                    st.json(grades)
                else:
                    st.info("No grades have been logged for this student yet.")
                break
        if not found:
            st.error("No student matches that Roll Number.")

# --- SEARCH TEACHER DETAILS ---
elif choice == "Search Teacher Details":
    st.subheader("🔍 Look Up Teacher Profile")
    search_id = st.text_input("Enter Employee ID to Search")

    if search_id:
        found = False
        for t in st.session_state.data["teachers"]:
            if t["emp_id"] == search_id:
                found = True
                st.success(f"Record found for {t['name']}!")
                st.write(f"**Name:** {t['name']}")
                st.write(f"**Employee ID:** {t['emp_id']}")
                st.write(f"**Subject Taught:** {t['subject']}")
                st.write(f"**Email:** {t['email']}")
                st.write(f"**Age:** {t['age']}")
                break
        if not found:
            st.error("No teacher matches that Employee ID.")
