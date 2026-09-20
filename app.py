import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="EduTrack AI - Analytics & Visualizations",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .auth-card {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    .brand-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {"admin": "admin123"}
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# Sample Student Dataset
if "student_data" not in st.session_state:
    st.session_state.student_data = [
        {"Student_ID": "STU1010", "Student_Name": "Meera Deshmukh", "Gender": "Female", "Department": "Data Science", "Semester": "Sem 6", "Subject": "Machine Learning", "Attendance_Percentage": 92.0, "Internal_Marks": 24, "Final_Exam_Marks": 95},
        {"Student_ID": "STU1004", "Student_Name": "Priya Patel", "Gender": "Female", "Department": "Computer Science", "Semester": "Sem 6", "Subject": "Data Structures", "Attendance_Percentage": 88.0, "Internal_Marks": 22, "Final_Exam_Marks": 92},
        {"Student_ID": "STU1020", "Student_Name": "Divya Menon", "Gender": "Female", "Department": "Computer Science", "Semester": "Sem 5", "Subject": "Algorithms", "Attendance_Percentage": 95.0, "Internal_Marks": 25, "Final_Exam_Marks": 90},
        {"Student_ID": "STU1014", "Student_Name": "Neha Gupta", "Gender": "Female", "Department": "Computer Science", "Semester": "Sem 4", "Subject": "Database Systems", "Attendance_Percentage": 85.0, "Internal_Marks": 20, "Final_Exam_Marks": 88},
        {"Student_ID": "STU1001", "Student_Name": "Aarav Sharma", "Gender": "Male", "Department": "Computer Science", "Semester": "Sem 6", "Subject": "Operating Systems", "Attendance_Percentage": 80.0, "Internal_Marks": 18, "Final_Exam_Marks": 85},
        {"Student_ID": "STU1003", "Student_Name": "Rohan Verma", "Gender": "Male", "Department": "Information Technology", "Semester": "Sem 5", "Subject": "Web Tech", "Attendance_Percentage": 65.0, "Internal_Marks": 14, "Final_Exam_Marks": 55},
        {"Student_ID": "STU1005", "Student_Name": "Vikram Singh", "Gender": "Male", "Department": "Electronics", "Semester": "Sem 4", "Subject": "Digital Logic", "Attendance_Percentage": 72.0, "Internal_Marks": 15, "Final_Exam_Marks": 60},
        {"Student_ID": "STU1011", "Student_Name": "Siddharth Das", "Gender": "Male", "Department": "Computer Science", "Semester": "Sem 5", "Subject": "Computer Networks", "Attendance_Percentage": 62.0, "Internal_Marks": 12, "Final_Exam_Marks": 58},
        {"Student_ID": "STU1013", "Student_Name": "Karan Malhotra", "Gender": "Male", "Department": "Electronics", "Semester": "Sem 6", "Subject": "VLSI Design", "Attendance_Percentage": 70.0, "Internal_Marks": 16, "Final_Exam_Marks": 64}
    ]

# -----------------------------------------------------------------------------
# AUTHENTICATION SCREEN
# -----------------------------------------------------------------------------
if not st.session_state.authenticated:
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.markdown("<div style='padding-top: 2rem;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='brand-title'>🎓 EduTrack AI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>Student Performance Analysis & Record Management System.</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("📊 **Track student records, semester grades, and subject progress in real-time.**")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        if st.session_state.auth_mode == "login":
            st.subheader("Welcome Back")
            login_user = st.text_input("Username", key="login_user_input", placeholder="e.g. admin")
            login_pass = st.text_input("Password", type="password", key="login_pass_input", placeholder="••••••••")
            
            if st.button("Sign In", type="primary", use_container_width=True):
                if login_user in st.session_state.user_db and st.session_state.user_db[login_user] == login_pass:
                    st.session_state.authenticated = True
                    st.session_state.current_user = login_user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            
            st.markdown("---")
            if st.button("Create an Account", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        else:
            st.subheader("Create an Account")
            reg_user = st.text_input("Choose Username", key="reg_user_input")
            reg_pass = st.text_input("Choose Password", type="password", key="reg_pass_input")
            reg_pass_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm_input")
            
            if st.button("Register Account", type="primary", use_container_width=True):
                if not reg_user or not reg_pass:
                    st.warning("Please fill in all fields.")
                elif reg_user in st.session_state.user_db:
                    st.error("Username already exists.")
                elif reg_pass != reg_pass_confirm:
                    st.error("Passwords do not match.")
                else:
                    st.session_state.user_db[reg_user] = reg_pass
                    st.success("Account created successfully!")
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            st.markdown("---")
            if st.button("Back to Login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN DASHBOARD WITH VISUALIZATIONS
# -----------------------------------------------------------------------------
else:
    # Sidebar Navigation & Management
    st.sidebar.title("🎓 EduTrack AI")
    st.sidebar.caption(f"Logged in as: **{st.session_state.current_user}**")
    
    if st.sidebar.button("Log Out", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Load DataFrame
    df = pd.DataFrame(st.session_state.student_data)

    # Global Filters
    st.sidebar.subheader("📌 Global Filters")
    dept_options = sorted(list(df["Department"].unique()))
    selected_depts = st.sidebar.multiselect("Filter Department", dept_options, default=dept_options)
    
    sem_options = sorted(list(df["Semester"].unique()))
    selected_sems = st.sidebar.multiselect("Filter Semester", sem_options, default=sem_options)
    
    # Action Selection: Add or Update
    st.sidebar.markdown("---")
    action = st.sidebar.radio("Choose Action", ["➕ Add New Student", "✏️ Update Existing Student"])

    if action == "➕ Add New Student":
        st.sidebar.subheader("➕ Add Student Record")
        with st.sidebar.form("add_student_form", clear_on_submit=True):
            new_id = st.text_input("Student ID", placeholder="e.g. STU1025")
            new_name = st.text_input("Student Name", placeholder="e.g. Rahul Sharma")
            new_gender = st.selectbox("Gender", ["Female", "Male", "Other"])
            new_dept = st.selectbox("Department", ["Data Science", "Computer Science", "Information Technology", "Electronics"])
            new_sem = st.selectbox("Semester", ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8"])
            new_subject = st.text_input("Subject", placeholder="e.g. Machine Learning")
            new_attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=85.0)
            new_internal = st.number_input("Internal Marks (Max 25)", min_value=0, max_value=25, value=20)
            new_final = st.number_input("Final Exam Marks (Max 100)", min_value=0, max_value=100, value=75)
            
            submit_btn = st.form_submit_button("Add Record", type="primary")
            if submit_btn:
                existing_ids = [s["Student_ID"] for s in st.session_state.student_data]
                if not new_id or not new_name or not new_subject:
                    st.sidebar.error("Student ID, Name, and Subject are required!")
                elif new_id in existing_ids:
                    st.sidebar.error("Student ID already exists!")
                else:
                    new_row = {
                        "Student_ID": new_id,
                        "Student_Name": new_name,
                        "Gender": new_gender,
                        "Department": new_dept,
                        "Semester": new_sem,
                        "Subject": new_subject,
                        "Attendance_Percentage": new_attendance,
                        "Internal_Marks": new_internal,
                        "Final_Exam_Marks": new_final
                    }
                    st.session_state.student_data.append(new_row)
                    st.sidebar.success(f"Added {new_name} ({new_id}) successfully!")
                    st.rerun()
    else:
        st.sidebar.subheader("✏️ Update Student Record")
        all_ids = [s["Student_ID"] for s in st.session_state.student_data]
        selected_id = st.sidebar.selectbox("Select Student ID to Update", all_ids)

        if selected_id:
            student_obj = next(s for s in st.session_state.student_data if s["Student_ID"] == selected_id)
            with st.sidebar.form("update_student_form"):
                up_name = st.text_input("Student Name", value=student_obj["Student_Name"])
                
                gender_idx = ["Female", "Male", "Other"].index(student_obj["Gender"]) if student_obj["Gender"] in ["Female", "Male", "Other"] else 0
                up_gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=gender_idx)
                
                dept_list = ["Data Science", "Computer Science", "Information Technology", "Electronics"]
                dept_idx = dept_list.index(student_obj["Department"]) if student_obj["Department"] in dept_list else 0
                up_dept = st.selectbox("Department", dept_list, index=dept_idx)
                
                sem_list = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8"]
                sem_idx = sem_list.index(student_obj["Semester"]) if student_obj["Semester"] in sem_list else 0
                up_sem = st.selectbox("Semester", sem_list, index=sem_idx)
                
                up_subject = st.text_input("Subject", value=student_obj["Subject"])
                up_attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=float(student_obj["Attendance_Percentage"]))
                up_internal = st.number_input("Internal Marks (Max 25)", min_value=0, max_value=25, value=int(student_obj["Internal_Marks"]))
                up_final = st.number_input("Final Exam Marks (Max 100)", min_value=0, max_value=100, value=int(student_obj["Final_Exam_Marks"]))
                
                update_btn = st.form_submit_button("Update Record", type="primary")
                if update_btn:
                    student_obj["Student_Name"] = up_name
                    student_obj["Gender"] = up_gender
                    student_obj["Department"] = up_dept
                    student_obj["Semester"] = up_sem
                    student_obj["Subject"] = up_subject
                    student_obj["Attendance_Percentage"] = up_attendance
                    student_obj["Internal_Marks"] = up_internal
                    student_obj["Final_Exam_Marks"] = up_final
                    st.sidebar.success(f"Updated details for {selected_id}!")
                    st.rerun()

    # Apply Filters
    if selected_depts and selected_sems:
        filtered_df = df[(df["Department"].isin(selected_depts)) & (df["Semester"].isin(selected_sems))]
    else:
        filtered_df = df.copy()

    # Title & Metrics
    st.title("📊 EduTrack AI - Dashboard Visualizations")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", len(filtered_df))
    m2.metric("Avg Attendance", f"{filtered_df['Attendance_Percentage'].mean():.1f}%" if not filtered_df.empty else "0%")
    m3.metric("Avg Final Score", f"{filtered_df['Final_Exam_Marks'].mean():.1f} / 100" if not filtered_df.empty else "0")
    m4.metric("Avg Internal Score", f"{filtered_df['Internal_Marks'].mean():.1f} / 25" if not filtered_df.empty else "0")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # VISUALIZATION CHARTS SECTION
    # -------------------------------------------------------------------------
    st.subheader("📈 Performance Analytics & Visual Charts")
    
    if not filtered_df.empty:
        # Row 1: Bar Chart & Scatter Plot
        col_fig1, col_fig2 = st.columns(2)
        
        with col_fig1:
            st.markdown("##### 🏢 Average Final Score by Department")
            dept_avg = filtered_df.groupby("Department")["Final_Exam_Marks"].mean().reset_index()
            fig_bar = px.bar(
                dept_avg, 
                x="Department", 
                y="Final_Exam_Marks", 
                color="Department",
                text_auto='.1f',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_bar.update_layout(showlegend=False, yaxis_title="Avg Final Marks")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_fig2:
            st.markdown("##### 🎯 Attendance vs. Final Marks Correlation")
            fig_scatter = px.scatter(
                filtered_df, 
                x="Attendance_Percentage", 
                y="Final_Exam_Marks",
                color="Department", 
                size="Internal_Marks", 
                hover_name="Student_Name",
                labels={"Attendance_Percentage": "Attendance (%)", "Final_Exam_Marks": "Final Exam Marks"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Row 2: Line Chart & Pie Chart
        col_fig3, col_fig4 = st.columns(2)

        with col_fig3:
            st.markdown("##### 📚 Semester Progress Marks Trend")
            sem_avg = filtered_df.groupby("Semester")[["Internal_Marks", "Final_Exam_Marks"]].mean().reset_index()
            fig_line = px.line(
                sem_avg, 
                x="Semester", 
                y=["Internal_Marks", "Final_Exam_Marks"],
                markers=True,
                labels={"value": "Marks", "variable": "Exam Type"}
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with col_fig4:
            st.markdown("##### 🍰 Grade Distribution Status")
            # Grading criteria logic
            def get_grade(mark):
                if mark >= 85: return "Distinction (>=85)"
                elif mark >= 70: return "First Class (70-84)"
                elif mark >= 50: return "Second Class (50-69)"
                else: return "Needs Improvement (<50)"
            
            filtered_df["Grade_Category"] = filtered_df["Final_Exam_Marks"].apply(get_grade)
            grade_counts = filtered_df["Grade_Category"].value_counts().reset_index()
            grade_counts.columns = ["Grade_Category", "Count"]

            fig_pie = px.pie(
                grade_counts, 
                names="Grade_Category", 
                values="Count", 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available to generate charts with current filters.")

    st.markdown("---")

    # Complete Student Dataset Table
    st.subheader("📋 Complete Student Dataset")
    search_query = st.text_input("🔍 Search student by Name, ID, or Subject:", "")
    
    if search_query:
        display_df = filtered_df[
            filtered_df["Student_Name"].str.contains(search_query, case=False, na=False) |
            filtered_df["Student_ID"].str.contains(search_query, case=False, na=False) |
            filtered_df["Subject"].str.contains(search_query, case=False, na=False)
        ]
    else:
        display_df = filtered_df

    st.dataframe(display_df, use_container_width=True, hide_index=True)