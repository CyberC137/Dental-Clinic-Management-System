import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
from openpyxl import Workbook
from functools import partial
import threading

# Database Setup
def setup_database():
    conn = sqlite3.connect('dental_clinic.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')

    # Create Patients table
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    contact TEXT
                )''')

    # Create Appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    date TEXT,
                    time TEXT,
                    description TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                )''')

    # Create Billing table
    c.execute('''CREATE TABLE IF NOT EXISTS billing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    date TEXT,
                    amount REAL,
                    description TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                )''')

    # Create a default admin user
    c.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)',
              ('admin', 'admin', 'admin'))

    conn.commit()
    conn.close()

setup_database()

# Main Application
class DentalClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental Clinic Management System")
        self.root.geometry("800x600")
        self.current_user_role = None
        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill='both', expand=True)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.username_entry = tk.Entry(self.login_frame)
        self.password_entry = tk.Entry(self.login_frame, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Button(self.login_frame, text="Login", command=self.authenticate_user).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('SELECT role FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.current_user_role = user[0]
            self.login_frame.destroy()
            self.create_main_interface()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def create_main_interface(self):
        self.tab_control = ttk.Notebook(self.root)
        self.tab_patients = ttk.Frame(self.tab_control)
        self.tab_appointments = ttk.Frame(self.tab_control)
        self.tab_billing = ttk.Frame(self.tab_control)
        self.tab_reports = ttk.Frame(self.tab_control)
        self.tab_users = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_patients, text='Patients')
        self.tab_control.add(self.tab_appointments, text='Appointments')
        self.tab_control.add(self.tab_billing, text='Billing')
        self.tab_control.add(self.tab_reports, text='Reports')

        if self.current_user_role == 'admin':
            self.tab_control.add(self.tab_users, text='Users')

        self.tab_control.pack(expand=1, fill='both')

        self.create_patients_tab()
        self.create_appointments_tab()
        self.create_billing_tab()
        self.create_reports_tab()
        if self.current_user_role == 'admin':
            self.create_users_tab()

    def create_users_tab(self):
        self.users_frame = tk.Frame(self.tab_users)
        self.users_frame.pack(fill='both', expand=True)

        tk.Label(self.users_frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.users_frame, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.users_frame, text="Role").grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.user_username = tk.Entry(self.users_frame)
        self.user_password = tk.Entry(self.users_frame)
        self.user_role = tk.Entry(self.users_frame)

        self.user_username.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.user_password.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.user_role.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Button(self.users_frame, text="Add User", command=self.add_user).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.users_frame, text="Update User", command=self.update_user).grid(row=3, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.users_frame, text="Delete User", command=self.delete_user).grid(row=3, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.users_frame, text="View Users", command=self.view_users).grid(row=3, column=3, padx=10, pady=10, sticky='w')

        self.user_tree = ttk.Treeview(self.users_frame, columns=("ID", "Username", "Role"), show='headings')
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        self.user_tree_scrollbar = ttk.Scrollbar(self.users_frame, orient='vertical', command=self.user_tree.yview)
        self.user_tree.configure(yscroll=self.user_tree_scrollbar.set)
        self.user_tree_scrollbar.grid(row=4, column=4, sticky='ns')

        self.users_frame.grid_rowconfigure(4, weight=1)
        self.users_frame.grid_columnconfigure(1, weight=1)

    def add_user(self):
        username = self.user_username.get()
        password = self.user_password.get()
        role = self.user_role.get()

        if not username or not password or not role:
            messagebox.showwarning("Warning", "All fields are required")
            return

        if role.lower() not in ["admin", "user"]:
            messagebox.showerror("Error", "Role must be 'admin' or 'user'")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully")
            self.view_users()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def update_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to update")
            return

        user_id = self.user_tree.item(selected_item)['values'][0]
        username = self.user_username.get()
        password = self.user_password.get()
        role = self.user_role.get()

        if not username or not password or not role:
            messagebox.showwarning("Warning", "All fields are required")
            return

        if role.lower() not in ["admin", "user"]:
            messagebox.showerror("Error", "Role must be 'admin' or 'user'")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?', (username, password, role, user_id))
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully")
            self.view_users()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        user_id = self.user_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            messagebox.showinfo("Success", "User deleted successfully")
            self.view_users()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def view_users(self):
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('SELECT id, username, role FROM users')
        users = c.fetchall()
        conn.close()
        self.user_tree.delete(*self.user_tree.get_children())
        for user in users:
            self.user_tree.insert('', 'end', values=user)

    def create_patients_tab(self):
        self.patients_frame = tk.Frame(self.tab_patients)
        self.patients_frame.pack(fill='both', expand=True)

        tk.Label(self.patients_frame, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Age").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Gender").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Contact").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Search").grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.patient_name = tk.Entry(self.patients_frame)
        self.patient_age = tk.Entry(self.patients_frame)
        self.patient_gender = tk.Entry(self.patients_frame)
        self.patient_contact = tk.Entry(self.patients_frame)
        self.search_patient_entry = tk.Entry(self.patients_frame)

        self.patient_name.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.patient_age.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.patient_gender.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.patient_contact.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.search_patient_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        tk.Button(self.patients_frame, text="Add Patient", command=self.add_patient).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="Update Patient", command=self.update_patient).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="Delete Patient", command=self.delete_patient).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="View Patients", command=self.view_patients).grid(row=4, column=3, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="Search", command=self.search_patients).grid(row=0, column=4, padx=10, pady=10, sticky='w')

        self.patient_tree = ttk.Treeview(self.patients_frame, columns=("ID", "Name", "Age", "Gender", "Contact"), show='headings')
        self.patient_tree.heading("ID", text="Patient ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("Contact", text="Contact")
        self.patient_tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.patient_tree_scrollbar = ttk.Scrollbar(self.patients_frame, orient='vertical', command=self.patient_tree.yview)
        self.patient_tree.configure(yscroll=self.patient_tree_scrollbar.set)
        self.patient_tree_scrollbar.grid(row=5, column=5, sticky='ns')

        self.patients_frame.grid_rowconfigure(5, weight=1)
        self.patients_frame.grid_columnconfigure(1, weight=1)

    def create_appointments_tab(self):
        self.appointments_frame = tk.Frame(self.tab_appointments)
        self.appointments_frame.pack(fill='both', expand=True)

        tk.Label(self.appointments_frame, text="Patient ID").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Date (DD-MM-YYYY)").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Time (HH:MM)").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Description").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Search").grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.appointment_patient_id = tk.Entry(self.appointments_frame)
        self.appointment_date = tk.Entry(self.appointments_frame)
        self.appointment_time = tk.Entry(self.appointments_frame)
        self.appointment_description = tk.Entry(self.appointments_frame)
        self.search_appointment_entry = tk.Entry(self.appointments_frame)

        self.appointment_patient_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.appointment_date.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.appointment_time.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.appointment_description.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.search_appointment_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        tk.Button(self.appointments_frame, text="Add Appointment", command=self.add_appointment).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="Update Appointment", command=self.update_appointment).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="Delete Appointment", command=self.delete_appointment).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="View Appointments", command=self.view_appointments).grid(row=4, column=3, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="Search", command=self.search_appointments).grid(row=0, column=4, padx=10, pady=10, sticky='w')

        self.appointment_tree = ttk.Treeview(self.appointments_frame, columns=("ID", "Patient ID", "Date", "Time", "Description"), show='headings')
        self.appointment_tree.heading("ID", text="S.No.")
        self.appointment_tree.heading("Patient ID", text="Patient ID")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Time", text="Time")
        self.appointment_tree.heading("Description", text="Description")
        self.appointment_tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.appointment_tree_scrollbar = ttk.Scrollbar(self.appointments_frame, orient='vertical', command=self.appointment_tree.yview)
        self.appointment_tree.configure(yscroll=self.appointment_tree_scrollbar.set)
        self.appointment_tree_scrollbar.grid(row=5, column=5, sticky='ns')

        self.appointments_frame.grid_rowconfigure(5, weight=1)
        self.appointments_frame.grid_columnconfigure(1, weight=1)

    def create_billing_tab(self):
        self.billing_frame = tk.Frame(self.tab_billing)
        self.billing_frame.pack(fill='both', expand=True)

        tk.Label(self.billing_frame, text="Patient ID").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Date (DD-MM-YYYY)").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Amount").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Description").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Search").grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.bill_patient_id = tk.Entry(self.billing_frame)
        self.bill_date = tk.Entry(self.billing_frame)
        self.bill_amount = tk.Entry(self.billing_frame)
        self.bill_description = tk.Entry(self.billing_frame)
        self.search_bill_entry = tk.Entry(self.billing_frame)

        self.bill_patient_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.bill_date.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.bill_amount.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.bill_description.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.search_bill_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        tk.Button(self.billing_frame, text="Generate Bill", command=self.add_bill).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="Update Bill", command=self.update_bill).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="Delete Bill", command=self.delete_bill).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="View Bills", command=self.view_bills).grid(row=4, column=3, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="Search", command=self.search_bills).grid(row=0, column=4, padx=10, pady=10, sticky='w')

        self.billing_tree = ttk.Treeview(self.billing_frame, columns=("ID", "Patient ID", "Date", "Amount", "Description"), show='headings')
        self.billing_tree.heading("ID", text="S.No.")
        self.billing_tree.heading("Patient ID", text="Patient ID")
        self.billing_tree.heading("Date", text="Date")
        self.billing_tree.heading("Amount", text="Amount")
        self.billing_tree.heading("Description", text="Description")
        self.billing_tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        self.billing_tree_scrollbar = ttk.Scrollbar(self.billing_frame, orient='vertical', command=self.billing_tree.yview)
        self.billing_tree.configure(yscroll=self.billing_tree_scrollbar.set)
        self.billing_tree_scrollbar.grid(row=5, column=5, sticky='ns')

        self.billing_frame.grid_rowconfigure(5, weight=1)
        self.billing_frame.grid_columnconfigure(1, weight=1)

    def create_reports_tab(self):
        self.reports_frame = tk.Frame(self.tab_reports)
        self.reports_frame.pack(fill='both', expand=True)

        tk.Button(self.reports_frame, text="Generate Patient Report", command=self.generate_patient_report).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.reports_frame, text="Generate Financial Report", command=self.generate_financial_report).grid(row=1, column=0, padx=10, pady=10)

    # Patient Management Methods
    def add_patient(self):
        name = self.patient_name.get()
        age = self.patient_age.get()
        gender = self.patient_gender.get()
        contact = self.patient_contact.get()

        if not name or not age or not gender or not contact:
            messagebox.showwarning("Warning", "All fields are required")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be a positive integer")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if gender.lower() not in ["male", "female", "other"]:
            messagebox.showerror("Error", "Gender must be 'Male', 'Female', or 'Other'")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO patients (name, age, gender, contact) VALUES (?, ?, ?, ?)', (name, age, gender, contact))
            conn.commit()
            messagebox.showinfo("Success", "Patient added successfully")
            self.view_patients()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def update_patient(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to update")
            return

        patient_id = self.patient_tree.item(selected_item)['values'][0]
        name = self.patient_name.get()
        age = self.patient_age.get()
        gender = self.patient_gender.get()
        contact = self.patient_contact.get()

        if not name or not age or not gender or not contact:
            messagebox.showwarning("Warning", "All fields are required")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be a positive integer")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if gender.lower() not in ["male", "female", "other"]:
            messagebox.showerror("Error", "Gender must be 'Male', 'Female', or 'Other'")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('UPDATE patients SET name = ?, age = ?, gender = ?, contact = ? WHERE id = ?', (name, age, gender, contact, patient_id))
            conn.commit()
            messagebox.showinfo("Success", "Patient updated successfully")
            self.view_patients()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def delete_patient(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return

        patient_id = self.patient_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
            conn.commit()
            messagebox.showinfo("Success", "Patient deleted successfully")
            self.view_patients()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def view_patients(self):
        def fetch_data():
            conn = sqlite3.connect('dental_clinic.db')
            c = conn.cursor()
            c.execute('SELECT * FROM patients')
            patients = c.fetchall()
            conn.close()
            self.patient_tree.delete(*self.patient_tree.get_children())
            for patient in patients:
                self.patient_tree.insert('', 'end', values=patient)

        threading.Thread(target=fetch_data).start()

    def search_patients(self):
        search_term = self.search_patient_entry.get()
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        query = "SELECT * FROM patients WHERE name LIKE ? OR ID LIKE ?"
        c.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
        patients = c.fetchall()
        conn.close()
        self.patient_tree.delete(*self.patient_tree.get_children())
        for patient in patients:
            self.patient_tree.insert('', 'end', values=patient)

    # Appointment Management Methods
    def add_appointment(self):
        patient_id = self.appointment_patient_id.get()
        date = self.appointment_date.get()
        time = self.appointment_time.get()
        description = self.appointment_description.get()

        if not patient_id or not date or not time or not description:
            messagebox.showwarning("Warning", "All fields are required")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO appointments (patient_id, date, time, description) VALUES (?, ?, ?, ?)', (patient_id, date, time, description))
            conn.commit()
            messagebox.showinfo("Success", "Appointment scheduled successfully")
            self.view_appointments()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def update_appointment(self):
        selected_item = self.appointment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return

        appointment_id = self.appointment_tree.item(selected_item)['values'][0]
        patient_id = self.appointment_patient_id.get()
        date = self.appointment_date.get()
        time = self.appointment_time.get()
        description = self.appointment_description.get()

        if not patient_id or not date or not time or not description:
            messagebox.showwarning("Warning", "All fields are required")
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('UPDATE appointments SET patient_id = ?, date = ?, time = ?, description = ? WHERE id = ?', (patient_id, date, time, description, appointment_id))
            conn.commit()
            messagebox.showinfo("Success", "Appointment updated successfully")
            self.view_appointments()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def delete_appointment(self):
        selected_item = self.appointment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return

        appointment_id = self.appointment_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Appointment deleted successfully")
            self.view_appointments()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def view_appointments(self):
        def fetch_data():
            conn = sqlite3.connect('dental_clinic.db')
            c = conn.cursor()
            c.execute('SELECT * FROM appointments')
            appointments = c.fetchall()
            conn.close()
            self.appointment_tree.delete(*self.appointment_tree.get_children())
            for appointment in appointments:
                self.appointment_tree.insert('', 'end', values=appointment)

        threading.Thread(target=fetch_data).start()

    def search_appointments(self):
        search_term = self.search_appointment_entry.get()
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        query = "SELECT * FROM appointments WHERE description LIKE ? OR patient_id LIKE ?"
        c.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
        appointments = c.fetchall()
        conn.close()
        self.appointment_tree.delete(*self.appointment_tree.get_children())
        for appointment in appointments:
            self.appointment_tree.insert('', 'end', values=appointment)

    # Billing Management Methods
    def add_bill(self):
        patient_id = self.bill_patient_id.get()
        date = self.bill_date.get()
        amount = self.bill_amount.get()
        description = self.bill_description.get()

        if not patient_id or not date or not amount or not description:
            messagebox.showwarning("Warning", "All fields are required")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO billing (patient_id, date, amount, description) VALUES (?, ?, ?, ?)', (patient_id, date, amount, description))
            conn.commit()
            messagebox.showinfo("Success", "Bill generated successfully")
            self.view_bills()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def update_bill(self):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a bill to update")
            return

        bill_id = self.billing_tree.item(selected_item)['values'][0]
        patient_id = self.bill_patient_id.get()
        date = self.bill_date.get()
        amount = self.bill_amount.get()
        description = self.bill_description.get()

        if not patient_id or not date or not amount or not description:
            messagebox.showwarning("Warning", "All fields are required")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('UPDATE billing SET patient_id = ?, date = ?, amount = ?, description = ? WHERE id = ?', (patient_id, date, amount, description, bill_id))
            conn.commit()
            messagebox.showinfo("Success", "Bill updated successfully")
            self.view_bills()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def delete_bill(self):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a bill to delete")
            return

        bill_id = self.billing_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        try:
            c.execute('DELETE FROM billing WHERE id = ?', (bill_id,))
            conn.commit()
            messagebox.showinfo("Success", "Bill deleted successfully")
            self.view_bills()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def view_bills(self):
        def fetch_data():
            conn = sqlite3.connect('dental_clinic.db')
            c = conn.cursor()
            c.execute('SELECT * FROM billing')
            bills = c.fetchall()
            conn.close()
            self.billing_tree.delete(*self.billing_tree.get_children())
            for bill in bills:
                self.billing_tree.insert('', 'end', values=bill)

        threading.Thread(target=fetch_data).start()

    def search_bills(self):
        search_term = self.search_bill_entry.get()
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        query = "SELECT * FROM billing WHERE description LIKE ? OR patient_id LIKE ?"
        c.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
        bills = c.fetchall()
        conn.close()
        self.billing_tree.delete(*self.billing_tree.get_children())
        for bill in bills:
            self.billing_tree.insert('', 'end', values=bill)

    # Reporting Methods
    def generate_patient_report(self):
        def generate_report():
            conn = sqlite3.connect('dental_clinic.db')
            patients_df = pd.read_sql_query('SELECT * FROM patients', conn)
            conn.close()
            patients_df.to_excel('patient_report.xlsx', index=False)
            messagebox.showinfo("Success", "Patient report generated successfully")

        threading.Thread(target=generate_report).start()

    def generate_financial_report(self):
        def generate_report():
            conn = sqlite3.connect('dental_clinic.db')
            billing_df = pd.read_sql_query('SELECT * FROM billing', conn)
            conn.close()
            billing_df.to_excel('financial_report.xlsx', index=False)
            messagebox.showinfo("Success", "Financial report generated successfully")

        threading.Thread(target=generate_report).start()

if __name__ == '__main__':
    root = tk.Tk()
    app = DentalClinicApp(root)
    root.mainloop()
