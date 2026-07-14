# School Management - full_combinatio2.py

This repository contains a simple school management script (full combinatio2.py) that allows a teacher to enter student marks, save them into an SQLite database and automatically generate PDF report cards for each student.

> NOTE: The script currently includes a hard-coded administrator username and password (ADMIN_USER and ADMIN_PASS). Treat this as a sample/demo only — do not use these credentials in production. See Security notes below.

## Features

- Interactive CLI login for a teacher (username/password).
- Batch entry of student marks for a class.
- Supports three stream combinations: Arts, Science, Computer Science (and a General fallback).
- Optional elective subjects (Sport Studies, Music, Agriculture, Commerce, Economics).
- Saves student records into an SQLite database (`school.db`) with the table `student_records`.
- Generates per-student PDF report cards including school logo (if a `logo.png` file is present) and class rank.
- Uses `fpdf` to render PDFs.

## Requirements

- Python 3.8+ (3.10 recommended)
- The following Python packages:
  - fpdf (pip install fpdf)
- No external database required — data is stored in a local SQLite database file `school.db`.

Install dependency:

```bash
pip install fpdf
```

## Files

- `full combinatio2.py` (main script)
- `school.db` (created automatically when the script runs)
- `logo.png` (optional — place a PNG file with this name next to the script to be included in PDFs)

## How it works

1. Run the script: `python "full combinatio2.py"`.
2. Log in with the administrator credentials (default credentials are in the script).
3. Enter the number of students in the class.
4. For each student, enter:
   - Student name
   - Marks for compulsory subjects: Mathematics, English, Business Studies, Geography, Kiswahili, Historia ya TZ & Maadili
   - Choose a stream combination and enter the stream-specific subject marks
   - Choose an elective (optional) and enter its marks
5. When data entry finishes, the script saves each student record in `school.db` and automatically generates PDF report cards for each student (files named `report_<Student_Name>.pdf`).

The PDF includes a header, school logo (if `logo.png` exists), the student's details, subject scores and grades, total, average, and class position/rank.

## Database schema

The script creates the following table in `school.db` if it does not already exist:

- `student_records` with columns:
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - name TEXT NOT NULL
  - combination TEXT
  - maths REAL
  - english REAL
  - business REAL
  - geography REAL
  - kiswahili REAL
  - historia_tz REAL
  - extra_sub1 REAL
  - extra_sub2 REAL
  - extra_sub3 REAL
  - elective_name TEXT
  - elective_score REAL
  - total REAL
  - average REAL

## Important notes & caveats

- Hard-coded credentials: ADMIN_USER and ADMIN_PASS are stored in plaintext in the script. For production use, remove these and use a secure authentication mechanism or an environment variable-based secret.

- Input validation: The script assumes the user enters valid numeric marks and does minimal validation. Consider adding validation (range checks, missing values handling) before storing data.

- Subject counts and average calculation: The script computes `num_subs` differently depending on stream and elective presence. Review logic if you add or remove subjects.

- Grades: The grade boundaries are defined in the `get_grade` function (A: 75+, B: 65+, C: 45+, D: 30+, else F). Adjust per your grading policy.

- File name: The main script contains a space in its filename (`full combinatio2.py`). To avoid issues on some OSes or automation tools, consider renaming it to `full_combinatio2.py` or `main.py`.

## Customization

- Logo: Add a `logo.png` file in the same folder if you want the school's logo printed on the PDF.

- Change admin credentials: Replace the `ADMIN_USER` and `ADMIN_PASS` variables in the script or load them from environment variables.

- PDF formatting: The script uses `fpdf` and basic layout calls. You can customize fonts, sizes, and layout in `make_pdf_report()`.

## Running non-interactively / automation

This script is interactive by design. If you want to automate data import (CSV or another DB), modify the script to add a CSV import path that reads many students and inserts into `student_records` directly. After records are in the database, you can call the `make_pdf_report(name)` function for each student name to generate PDFs.

## Troubleshooting

- If PDFs are blank or fonts fail, ensure `fpdf` is installed and that the environment has access to write files in the working directory.

- If the script cannot find `logo.png`, it prints a tip and continues generating PDFs without a logo.

- If you get crashes on numeric conversion, double-check that you are entering numeric marks (floats/integers) when prompted.

## Suggested improvements

- Replace plaintext credentials with environment variables or a proper authentication module.
- Add robust input validation and error handling.
- Add an option to export/import CSV.
- Use UUIDs or student admission numbers instead of names as the main lookup key to avoid collisions when students share names.
- Add unit tests for the grade, ranking and PDF generation functions.

## License

This project is provided as-is for educational/demo purposes. Add a license file if you plan to publish or reuse this commercially.
