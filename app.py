import streamlit as st

# Employee Login
employee_signin = {'140520': 'MICK1', '140521': 'MICK2', '140522': 'MICK3'}

# Initialize patients in session_state
if 'patients' not in st.session_state:
    st.session_state.patients = {
        '1145980': ['Name: Michael Smith', 'Gender: Male', 'Age: 28', "Address: 100 Main St Atlanta GA", "Diagnosis: Flu", "Treatment: Antiviral Medication"],
        '1145981': ['Name: Mary Brown', 'Gender: Female', 'Age: 32', "Address: 251 Spring Street Kennesaw GA", "Diagnosis: Cold", "Treatment: Rest and Hydration"],
    }

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("Employee Login")
    emp_id = st.text_input("Employee ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if emp_id in employee_signin and employee_signin[emp_id] == password:
            st.session_state.logged_in = True
            st.session_state.user = emp_id
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")
else:
    st.title("Welcome to the OPEN EMR System")
    st.write(f"Logged in as Employee ID: {st.session_state.user}")

    # --- REGISTER PATIENT ---
    st.subheader("Register Patient")
    with st.expander("Add New Patient"):
        new_mrn = st.text_input("MRN")
        new_name = st.text_input("Name")
        new_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        new_age = st.number_input("Age", min_value=0, max_value=120)
        new_address = st.text_input("Address")
        new_diagnosis = st.text_input("Diagnosis")
        new_treatment = st.text_input("Treatment")
        if st.button("Register Patient"):
            if new_mrn in st.session_state.patients:
                st.warning("Patient already exists!")
            else:
                st.session_state.patients[new_mrn] = [
                    f"Name: {new_name}",
                    f"Gender: {new_gender}",
                    f"Age: {new_age}",
                    f"Address: {new_address}",
                    f"Diagnosis: {new_diagnosis}",
                    f"Treatment: {new_treatment}"
                ]
                st.success(f"Patient {new_name} registered successfully!")

    # --- UPDATE PATIENT ---
    st.subheader("Update Patient")
    with st.expander("Update Existing Patient"):
        update_mrn = st.text_input("MRN to Update")
        if update_mrn in st.session_state.patients:
            st.write("Current Details:")
            for detail in st.session_state.patients[update_mrn]:
                st.write(detail)

            field_to_update = st.selectbox("Field to Update", ["Name", "Gender", "Age", "Address", "Diagnosis", "Treatment"])
            new_value = st.text_input(f"Enter new value for {field_to_update}")
            if st.button("Update Patient"):
                field_map = {"Name": 0, "Gender": 1, "Age": 2, "Address": 3, "Diagnosis": 4, "Treatment": 5}
                index = field_map[field_to_update]
                st.session_state.patients[update_mrn][index] = f"{field_to_update}: {new_value}"
                st.success(f"{field_to_update} updated successfully!")
        else:
            if update_mrn:
                st.warning("Patient MRN not found")

    # --- DELETE PATIENT ---
    st.subheader("Delete Patient")
    delete_mrn = st.text_input("Enter MRN to Delete")
    if st.button("Delete Patient"):
        if delete_mrn in st.session_state.patients:
            del st.session_state.patients[delete_mrn]
            st.success(f"Patient {delete_mrn} deleted successfully!")
        else:
            st.error("Patient not found!")

    # --- LIST ALL PATIENTS ---
    st.subheader("All Patients")
    if st.button("Show All Patients"):
        for mrn, details in st.session_state.patients.items():
            st.write(f"MRN: {mrn}")
            for d in details:
                st.write(d)
            st.write("---")

    # --- LOGOUT ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()
