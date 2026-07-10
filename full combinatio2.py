import sqlite3
import os
from fpdf import FPDF

# --- 1. CONNECT TO DATABASE & CREATE THE TABLE ---
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    combination TEXT,
    maths REAL, english REAL, business REAL, geography REAL, kiswahili REAL, historia_tz REAL,
    extra_sub1 REAL, extra_sub2 REAL, extra_sub3 REAL, elective_name TEXT, elective_score REAL,
    total REAL, average REAL
)
""")
conn.commit()


# --- 2. AUTOMATIC GRADE CONVERTER FUNCTION ---
def get_grade(score):
    if score >= 75: return "A"
    elif score >= 65: return "B"
    elif score >= 45: return "C"
    elif score >= 30: return "D"
    else: return "F"


# --- 3. CLASS RANKING CALCULATION FUNCTION ---
# This looks at everyone in the database and finds a student's rank position
def get_student_rank(student_name):
    cursor.execute("SELECT name FROM student_records ORDER BY average DESC")
    all_ranked_students = cursor.fetchall()
    
    # Loop through the ranked list to find the student's spot
    for position, row in enumerate(all_ranked_students, start=1):
        if row[0] == student_name:
            return position
            
    return "N/A"  # Returns this if the student is not found


# --- 4. PREMIUM PDF GENERATION PROCESSOR (WITH LOGO & RANK) ---
def make_pdf_report(student_name):
    cursor.execute("SELECT * FROM student_records WHERE name = ? ORDER BY id DESC", (student_name,))
    student_data = cursor.fetchone()
                    
    if not student_data:
        print(f"Error: Could not find data for {student_name} to build the PDF.")
        return
    
    # Unpack columns
    id, jina, combi, m, e, b, g, k, h, ex1, ex2, ex3, elec_name, elec_score, total, average = student_data
    
    # Calculate the student's rank position in the entire school database
    rank = get_student_rank(jina) 
    cursor.execute("SELECT COUNT(*) FROM student_records")
    total_class_size = cursor.fetchone()[0]
    
    pdf = FPDF()
    pdf.add_page()
    
    # --- ADD THE SCHOOL LOGO ---
    # This checks if logo.png exists in your folder before placing it
    if os.path.exists("logo.png"):
        # parameters: image_path, x_coordinate, y_coordinate, width
        pdf.image("logo.png", x=10, y=10, w=30)
        pdf.ln(15)  # Add some blank space below the logo line
    else:
        print("💡 Tip: Save a picture named 'logo.png' in this folder to print it on the PDF!")
    
    # Title Layout
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, text="OFFICIAL STUDENT REPORT CARD", ln=1, align='C')
    pdf.ln(10)
   
    # Student Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, text=f"Student Name: {jina}", ln=1)
    pdf.cell(200, 8, text=f"Combination: {combi}", ln=1)
    pdf.cell(200, 8, text=f"Database System ID: {id}", ln=1)
    
    # --- DISPLAY THE CALCULATED RANK ---
    pdf.set_text_color(0, 102, 204)  # Make the rank stand out in a nice blue text
    pdf.cell(200, 8, text=f"Class Position / Rank: {rank} out of {total_class_size} students", ln=1)
    pdf.set_text_color(0, 0, 0)      # Reset color back to plain black
    pdf.ln(5)
   
    # Table Header
    pdf.cell(60, 10, "Subject", 1, align='C')
    pdf.cell(40, 10, "Score", 1, align='C')
    pdf.cell(40, 10, "Grade", 1, align='C')
    pdf.ln()
   
    pdf.set_font("Arial", size=12)
    pdf.ln(0)
    
    # Base subjects list
    subjects = [
        ("Mathematics", m), ("English", e), ("Business Studies", b),
        ("Geography", g), ("Kiswahili", k), ("Historia ya TZ & Maadili", h)
    ]
    
    # Append stream specific subjects
    if combi == "Arts":
        subjects.extend([("History", ex1), ("Biology", ex2)])
    elif combi == "Science":
        subjects.extend([("Chemistry", ex1), ("Biology", ex2), ("Physics", ex3)])
    elif combi == "Computer Science":
        subjects.extend([("Computer Science", ex1), ("Additional Maths", ex2), ("Physics", ex3)])

    # Append elective subject if they took one
    if elec_name != "None":
        subjects.append((elec_name, elec_score))

    # Print rows into PDF
    for somo, alama in subjects:
        pdf.cell(60, 10, somo, 1)
        pdf.cell(40, 10, str(alama), 1, align='C')
        pdf.cell(40, 10, get_grade(alama), 1, align='C')
        pdf.ln()
   
    # Overall Performance Box
    pdf.ln(0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Total Marks", 1)
    pdf.cell(40, 10, str(total), 1, align='C')
    pdf.ln()
    pdf.cell(60, 10, "Average Score", 1)
    pdf.cell(40, 10, f"{average:.1f}%", 1, align='C')
    pdf.ln()
    pdf.cell(60, 10, "Final Grade Status", 1)
    pdf.cell(40, 10, get_grade(average), 1, align='C')
    
    # Save file automatically using the student's name
    safe_name = jina.replace(' ', '_')
    filename = f"report_{safe_name}.pdf"
    pdf.output(filename)
    print(f"🎉 PDF Created Successfully with Rank and Logo: {filename}")


# --- 5. SECURE LOGIN SCREEN ---
print("=========================================")
print("  SCHOOL MANAGEMENT SYSTEM - LOGIN SCREEN")
print("=========================================")

ADMIN_USER = "proffesionalIT"
ADMIN_PASS = "begin@2026"

username = input("Enter Username: ")
password = input("Enter Password: ")

if username == ADMIN_USER and password == ADMIN_PASS:
    print("\n✅ Login Successful! Welcome back, Teacher.\n")
    
    num_students = int(input("How many students are in the class today? "))
    current_batch_names = []
    
    # --- 6. DATA ENTRY LOOP ---
    for i in range(num_students):
        print(f"\n-----------------------------------------")
        print(f"🎒 ENTERING DETAILS FOR STUDENT {i + 1} OF {num_students}")
        print(f"-----------------------------------------")
        
        student = str(input("Enter student name: "))
        current_batch_names.append(student)
        
        maths = float(input("Mathematics marks: "))
        english = float(input("English marks: "))
        business_studies = float(input("Business studies marks: "))
        geography = float(input("Geography marks: "))
        kiswahili = float(input("Kiswahili marks: "))
        historia_ya_tz_na_maadili = float(input("Historia ya TZ na Maadili marks: "))

        compulsory = maths + english + kiswahili + geography + business_studies + historia_ya_tz_na_maadili

        def get_elective():
            print("\n--- CHOOSE AN ELECTIVE SUBJECT ---")
            print("1. Sport Studies | 2. Music | 3. Agriculture | 4. Commerce | 5. Economics | 6. No Extra Subject")
            choice = input("Choose 1-6: ")
            if choice == "1": return "Sport Studies", float(input("Sport studies marks: "))
            elif choice == "2": return "Music", float(input("Music marks: "))
            elif choice == "3": return "Agriculture", float(input("Agriculture marks: "))
            elif choice == "4": return "Commerce", float(input("Commerce marks: "))
            elif choice == "5": return "Economics", float(input("Economics marks: "))
            else: return "None", 0.0

        print("\n--- CHOOSE YOUR COMBINATION ---")
        print("1. Arts | 2. Science | 3. Computer science")
        option = input("Choose 1, 2 or 3: ")

        ex1, ex2, ex3 = None, None, None
        combi_name = ""

        if option == "1":
            combi_name = "Arts"
            ex1 = float(input("History marks: "))
            ex2 = float(input("Biology marks: "))
            elective_name, elective_score = get_elective()
            total = compulsory + ex1 + ex2 + elective_score
            num_subs = 9 if elective_name != "None" else 8
        elif option == "2":
            combi_name = "Science"
            ex1 = float(input("Chemistry marks: "))
            ex2 = float(input("Biology marks: "))
            ex3 = float(input("Physics marks: "))
            elective_name, elective_score = get_elective()
            total = compulsory + ex1 + ex2 + ex3 + elective_score
            num_subs = 10 if elective_name != "None" else 9
        elif option == "3":
            combi_name = "Computer Science"
            ex1 = float(input("Computer Science marks: "))
            ex2 = float(input("Additional Mathematics marks: "))
            ex3 = float(input("Physics marks: "))
            elective_name, elective_score = get_elective()
            total = compulsory + ex1 + ex2 + ex3 + elective_score
            num_subs = 10 if elective_name != "None" else 9
        else:
            combi_name = "General"
            elective_name, elective_score = "None", 0.0
            total = compulsory
            num_subs = 6

        average = total / num_subs

        # Save to SQLite
        cursor.execute("""
            INSERT INTO student_records (name, combination, maths, english, business, geography, kiswahili, historia_tz, extra_sub1, extra_sub2, extra_sub3, elective_name, elective_score, total, average)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student, combi_name, maths, english, business_studies, geography, kiswahili, historia_ya_tz_na_maadili, ex1, ex2, ex3, elective_name, elective_score, total, average))
        conn.commit()
        print("💾 Record saved successfully!")

    # --- 7. AUTOMATED BATCH PDF GENERATION ---
    print("\n================ GENERATING PDF REPORT CARDS =================")
    for name in current_batch_names:
        make_pdf_report(name)
        
    print("\n🎉 All database records updated and PDF files generated successfully!")

else:
    print("\n❌ Invalid Username or Password! Access Denied.")

# Close connection safely
conn.close()
