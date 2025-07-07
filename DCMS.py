import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
from openpyxl import Workbook

# Database Setup
def setup_database():
    conn = sqlite3.connect('dental_clinic.db')
    c = conn.cursor()
    
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
    
    conn.commit()
    conn.close()

setup_database()

# Main Application
class DentalClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental Clinic Management System")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab_patients = ttk.Frame(self.tab_control)
        self.tab_appointments = ttk.Frame(self.tab_control)
        self.tab_billing = ttk.Frame(self.tab_control)
        self.tab_reports = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_patients, text='Patients')
        self.tab_control.add(self.tab_appointments, text='Appointments')
        self.tab_control.add(self.tab_billing, text='Billing')
        self.tab_control.add(self.tab_reports, text='Reports')

        self.tab_control.pack(expand=1, fill='both')

        self.create_patients_tab()
        self.create_appointments_tab()
        self.create_billing_tab()
        self.create_reports_tab()

    def create_patients_tab(self):
        # Patient Management Widgets
        self.patients_frame = tk.Frame(self.tab_patients)
        self.patients_frame.pack(fill='both', expand=True)

        # Labels and Entries
        tk.Label(self.patients_frame, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Age").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Gender").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.patients_frame, text="Contact").grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.patient_name = tk.Entry(self.patients_frame)
        self.patient_age = tk.Entry(self.patients_frame)
        self.patient_gender = tk.Entry(self.patients_frame)
        self.patient_contact = tk.Entry(self.patients_frame)

        self.patient_name.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.patient_age.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.patient_gender.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.patient_contact.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Buttons
        tk.Button(self.patients_frame, text="Add Patient", command=self.add_patient).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="Update Patient", command=self.update_patient).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="Delete Patient", command=self.delete_patient).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.patients_frame, text="View Patients", command=self.view_patients).grid(row=4, column=3, padx=10, pady=10, sticky='w')

        # Treeview
        self.patient_tree = ttk.Treeview(self.patients_frame, columns=("ID", "Name", "Age", "Gender", "Contact"), show='headings')
        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("Contact", text="Contact")
        self.patient_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Add vertical scrollbar to the treeview
        self.patient_tree_scrollbar = ttk.Scrollbar(self.patients_frame, orient='vertical', command=self.patient_tree.yview)
        self.patient_tree.configure(yscroll=self.patient_tree_scrollbar.set)
        self.patient_tree_scrollbar.grid(row=5, column=4, sticky='ns')

        # Configure grid weights for the treeview to expand correctly
        self.patients_frame.grid_rowconfigure(5, weight=1)
        self.patients_frame.grid_columnconfigure(1, weight=1)

    def create_appointments_tab(self):
        # Appointment Management Widgets
        self.appointments_frame = tk.Frame(self.tab_appointments)
        self.appointments_frame.pack(fill='both', expand=True)

        # Labels and Entries
        tk.Label(self.appointments_frame, text="Patient ID").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Time (HH:MM)").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.appointments_frame, text="Description").grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.appointment_patient_id = tk.Entry(self.appointments_frame)
        self.appointment_date = tk.Entry(self.appointments_frame)
        self.appointment_time = tk.Entry(self.appointments_frame)
        self.appointment_description = tk.Entry(self.appointments_frame)

        self.appointment_patient_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.appointment_date.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.appointment_time.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.appointment_description.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Buttons
        tk.Button(self.appointments_frame, text="Add Appointment", command=self.add_appointment).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="Update Appointment", command=self.update_appointment).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="Delete Appointment", command=self.delete_appointment).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.appointments_frame, text="View Appointments", command=self.view_appointments).grid(row=4, column=3, padx=10, pady=10, sticky='w')

        # Treeview
        self.appointment_tree = ttk.Treeview(self.appointments_frame, columns=("ID", "Patient ID", "Date", "Time", "Description"), show='headings')
        self.appointment_tree.heading("ID", text="ID")
        self.appointment_tree.heading("Patient ID", text="Patient ID")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Time", text="Time")
        self.appointment_tree.heading("Description", text="Description")
        self.appointment_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Add vertical scrollbar to the treeview
        self.appointment_tree_scrollbar = ttk.Scrollbar(self.appointments_frame, orient='vertical', command=self.appointment_tree.yview)
        self.appointment_tree.configure(yscroll=self.appointment_tree_scrollbar.set)
        self.appointment_tree_scrollbar.grid(row=5, column=4, sticky='ns')

        # Configure grid weights for the treeview to expand correctly
        self.appointments_frame.grid_rowconfigure(5, weight=1)
        self.appointments_frame.grid_columnconfigure(1, weight=1)

    def create_billing_tab(self):
        # Billing Management Widgets
        self.billing_frame = tk.Frame(self.tab_billing)
        self.billing_frame.pack(fill='both', expand=True)

        # Labels and Entries
        tk.Label(self.billing_frame, text="Patient ID").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Amount").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.billing_frame, text="Description").grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.bill_patient_id = tk.Entry(self.billing_frame)
        self.bill_date = tk.Entry(self.billing_frame)
        self.bill_amount = tk.Entry(self.billing_frame)
        self.bill_description = tk.Entry(self.billing_frame)

        self.bill_patient_id.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.bill_date.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.bill_amount.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.bill_description.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Buttons
        tk.Button(self.billing_frame, text="Generate Bill", command=self.add_bill).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="Update Bill", command=self.update_bill).grid(row=4, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="Delete Bill", command=self.delete_bill).grid(row=4, column=2, padx=10, pady=10, sticky='w')
        tk.Button(self.billing_frame, text="View Bills", command=self.view_bills).grid(row=4, column=3, padx=10, pady=10, sticky='w')

        # Treeview
        self.billing_tree = ttk.Treeview(self.billing_frame, columns=("ID", "Patient ID", "Date", "Amount", "Description"), show='headings')
        self.billing_tree.heading("ID", text="ID")
        self.billing_tree.heading("Patient ID", text="Patient ID")
        self.billing_tree.heading("Date", text="Date")
        self.billing_tree.heading("Amount", text="Amount")
        self.billing_tree.heading("Description", text="Description")
        self.billing_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Add vertical scrollbar to the treeview
        self.billing_tree_scrollbar = ttk.Scrollbar(self.billing_frame, orient='vertical', command=self.billing_tree.yview)
        self.billing_tree.configure(yscroll=self.billing_tree_scrollbar.set)
        self.billing_tree_scrollbar.grid(row=5, column=4, sticky='ns')

        # Configure grid weights for the treeview to expand correctly
        self.billing_frame.grid_rowconfigure(5, weight=1)
        self.billing_frame.grid_columnconfigure(1, weight=1)

    def create_reports_tab(self):
        # Reporting Widgets
        self.reports_frame = tk.Frame(self.tab_reports)
        self.reports_frame.pack(fill='both', expand=True)

        # Buttons
        tk.Button(self.reports_frame, text="Generate Patient Report", command=self.generate_patient_report).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.reports_frame, text="Generate Financial Report", command=self.generate_financial_report).grid(row=1, column=0, padx=10, pady=10)

    # Patient Management Methods
    def add_patient(self):
        name = self.patient_name.get()
        age = self.patient_age.get()
        gender = self.patient_gender.get()
        contact = self.patient_contact.get()
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('INSERT INTO patients (name, age, gender, contact) VALUES (?, ?, ?, ?)', (name, age, gender, contact))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient added successfully")
        self.view_patients()

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
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('UPDATE patients SET name = ?, age = ?, gender = ?, contact = ? WHERE id = ?', (name, age, gender, contact, patient_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient updated successfully")
        self.view_patients()

    def delete_patient(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        patient_id = self.patient_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient deleted successfully")
        self.view_patients()

    def view_patients(self):
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('SELECT * FROM patients')
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
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('INSERT INTO appointments (patient_id, date, time, description) VALUES (?, ?, ?, ?)', (patient_id, date, time, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Appointment scheduled successfully")
        self.view_appointments()

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
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('UPDATE appointments SET patient_id = ?, date = ?, time = ?, description = ? WHERE id = ?', (patient_id, date, time, description, appointment_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Appointment updated successfully")
        self.view_appointments()

    def delete_appointment(self):
        selected_item = self.appointment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return
        
        appointment_id = self.appointment_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Appointment deleted successfully")
        self.view_appointments()

    def view_appointments(self):
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('SELECT * FROM appointments')
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
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('INSERT INTO billing (patient_id, date, amount, description) VALUES (?, ?, ?, ?)', (patient_id, date, amount, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Bill generated successfully")
        self.view_bills()

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
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('UPDATE billing SET patient_id = ?, date = ?, amount = ?, description = ? WHERE id = ?', (patient_id, date, amount, description, bill_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Bill updated successfully")
        self.view_bills()

    def delete_bill(self):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a bill to delete")
            return
        
        bill_id = self.billing_tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('DELETE FROM billing WHERE id = ?', (bill_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Bill deleted successfully")
        self.view_bills()

    def view_bills(self):
        conn = sqlite3.connect('dental_clinic.db')
        c = conn.cursor()
        c.execute('SELECT * FROM billing')
        bills = c.fetchall()
        conn.close()
        self.billing_tree.delete(*self.billing_tree.get_children())
        for bill in bills:
            self.billing_tree.insert('', 'end', values=bill)

    # Reporting Methods
    def generate_patient_report(self):
        conn = sqlite3.connect('dental_clinic.db')
        patients_df = pd.read_sql_query('SELECT * FROM patients', conn)
        conn.close()
        patients_df.to_excel('patient_report.xlsx', index=False)
        messagebox.showinfo("Success", "Patient report generated successfully")

    def generate_financial_report(self):
        conn = sqlite3.connect('dental_clinic.db')
        billing_df = pd.read_sql_query('SELECT * FROM billing', conn)
        conn.close()
        billing_df.to_excel('financial_report.xlsx', index=False)
        messagebox.showinfo("Success", "Financial report generated successfully")

if __name__ == '__main__':
    root = tk.Tk()
    app = DentalClinicApp(root)
    root.mainloop()