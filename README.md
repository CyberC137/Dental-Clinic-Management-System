# Dental Clinic Management System

A desktop application built with Python and Tkinter for managing patients, appointments, billing, and reports for a dental clinic. It uses SQLite for data storage and pandas/openpyxl for exporting reports to Excel.

## Features

* **Patient Management**: Add, update, delete, and view patient records.
* **Appointment Scheduling**: Schedule, modify, cancel, and view appointments.
* **Billing System**: Generate, update, delete, and review billing entries.
* **Reporting**:

  * Export patient details to `patient_report.xlsx`.
  * Export financial/billing data to `financial_report.xlsx`.

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Database Setup](#database-setup)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)

## Requirements

* Python 3.7 or higher
* The following Python packages:

  * `tkinter` (usually included with Python)
  * `sqlite3` (standard library)
  * `pandas`
  * `openpyxl`

Install dependencies with:

```bash
pip install pandas openpyxl
```

## Installation

1. Clone this repository
2. Ensure dependencies are installed (see [Requirements](#requirements)).
3. Run the application:
   ```bash
python DCMS.py
````

## Database Setup

On first run, the application automatically creates an SQLite database file named `dental_clinic.db` in the working directory, with the following tables:

* **patients**:

  * `id` (INTEGER, primary key)
  * `name` (TEXT)
  * `age` (INTEGER)
  * `gender` (TEXT)
  * `contact` (TEXT)
* **appointments**:

  * `id` (INTEGER, primary key)
  * `patient_id` (INTEGER, foreign key → patients.id)
  * `date` (TEXT, YYYY-MM-DD)
  * `time` (TEXT, HH\:MM)
  * `description` (TEXT)
* **billing**:

  * `id` (INTEGER, primary key)
  * `patient_id` (INTEGER, foreign key → patients.id)
  * `date` (TEXT, YYYY-MM-DD)
  * `amount` (REAL)
  * `description` (TEXT)

## Usage

1. **Patients Tab**:

   * **Add Patient**: Enter name, age, gender, contact, then click **Add Patient**.
   * **Update Patient**: Select a record from the list, edit fields, then click **Update Patient**.
   * **Delete Patient**: Select a record and click **Delete Patient**.
   * **View Patients**: Refresh the list view.

2. **Appointments Tab**:

   * **Add Appointment**: Enter patient ID, date, time, description, then click **Add Appointment**.
   * **Update Appointment**:, **Delete Appointment**, **View Appointments** similar to Patients.

3. **Billing Tab**:

   * **Generate Bill**: Enter patient ID, date, amount, description, then click **Generate Bill**.
   * **Update Bill**, **Delete Bill**, **View Bills** similar to above.

4. **Reports Tab**:

   * **Generate Patient Report**: Exports all patients to `patient_report.xlsx`.
   * **Generate Financial Report**: Exports all billing entries to `financial_report.xlsx`.

## Project Structure

```
├── DCMS.py             # Main application script
├── dental_clinic.db    # Auto-generated SQLite database
├── patient_report.xlsx # Generated patient report
├── financial_report.xlsx # Generated billing report
└── README.md           # Project documentation
```

## Contributing

Contributions are welcome! To propose changes:

1. Fork this repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes and push: `git push origin feature/YourFeature`.
4. Open a Pull Request describing your improvements.

## Disclaimer

This project is for demonstration and educational use only. Use responsibly and do not deploy with real funds without proper testing.

---
