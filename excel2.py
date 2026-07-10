import os
import sqlite3
import pandas as pd
from fpdf import FPDF

# --- 1. CONFIGURATION AND CONFIG DATABASE ---
def init_db():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_data(
        name TEXT NOT NULL,
        total_marks REAL,
        average REAL,
        division TEXT,
        rank INTEGER
    )""")
    conn.commit()
    return conn

# --- 2. DYNAMIC GRADING AND CLASS TEACHER REMARKS ---
def get_grade_and_remark(score):
    """Returns the Grade and Swahili Remark based on the total score out of 100."""
    if pd.isna(score):
        return "-", "Hakuna Alama"
        
    if score >= 75: 
        return "A", "Vizuri Sana (Excellent). Ameweka juhudi kubwa."
    elif score >= 65: 
        return "B", "Vizuri (Very Good). Ana uwezo mzuri akijituma zaidi."
    elif score >= 45: 
        return "C", "Amefaulu (Good). Ongeza bidii kuongeza alama."
    elif score >= 30: 
        return "D", "Inaridhisha (Satisfactory). Shauriwa kukaza mwendo."
    else: 
        return "F", "Feli (Failed). Inahitajika jitihada za makusudi."

def get_headteacher_remark(average):
    """Generates headmaster comments dynamically based on the final average score."""
    if average >= 75:
        return "Maoni ya Mkuu wa Shule: Hongera sana! Mwanafunzi amedhihirisha kipaji na nidhamu ya hali ya juu."
    elif average >= 50:
        return "Maoni ya Mkuu wa Shule: Kazi nzuri. Mwanafunzi anaweza kufanya vizuri zaidi akiongeza bidii."
    else:
        return "Maoni ya Mkuu wa Shule: Inabidi mwanafunzi asaidiwe kwa ukaribu nyumbani na shuleni ili kurejesha ari."

# --- 3. DYNAMIC PDF GENERATOR ENGINE ---
def make_pdf(student_row, rank, total_students, subject_list):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Logos
    if os.path.exists("photo.jpg"):
        pdf.image('photo.jpg', x=20, y=10, w=24)
    if os.path.exists('image.jpg'):
        pdf.image('image.jpg', x=160, y=10, w=24)
        
    pdf.ln(10)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 4, "WIZARA YA ELIMU, SAYANSI NA TEKNOLOJIA", ln=1, align="C")
    pdf.cell(190, 5, "SHULE YA SEKONDARI WAANGWARAY", ln=1, align="C")
    pdf.cell(190, 5, "TAARIFA YA MAENDELEO YA TAALUMA NA NIDHAMU YA MWANAFUNZI", ln=1, align="C")
    pdf.ln(10)
    
    # Student Metadata
    pdf.set_font("Arial", "B", 9)
    pdf.cell(190, 5, f"JINA LA MWANAFUNZI: {str(student_row['name']).upper()}", ln=1, align="L")
    pdf.cell(190, 5, "KIDATO CHA PILI", ln=1, align="L")
    pdf.cell(190, 5, "MUHULA WA II MWAKA 2026", ln=1, align="L")
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(190, 5, "A: TAALUMA", ln=1, align="L")
    pdf.ln(2)
    
    # Table Grid Header
    pdf.set_font("Arial", "B", 9)
    pdf.cell(40, 8, "MASOMO", 1, 0, "C")
    pdf.cell(20, 8, "MAZOEZI", 1, 0, "C")
    pdf.cell(20, 8, "MTIHANI", 1, 0, "C")
    pdf.cell(20, 8, "JUMLA", 1, 0, "C")
    pdf.cell(15, 8, "GRED", 1, 0, "C")
    pdf.cell(60, 8, "MAONI YA MWALIMU WA SOMO", 1, 0, "C")
    pdf.cell(15, 8, "SAHIHI", 1, 1, "C")
    
    pdf.set_font("Arial", "", 9)
    
    # Dynamic Subject Loop Builder
    for sub in subject_list:
        mazoezi_score = student_row.get(f"{sub}_mazoezi", 0)
        mitihani_score = student_row.get(f"{sub}_mitihani", 0)
        
        # Fill missing NaN cells safely
        if pd.isna(mazoezi_score): mazoezi_score = 0
        if pd.isna(mitihani_score): mitihani_score = 0
        
        jumla = mazoezi_score + mitihani_score
        grade, remark = get_grade_and_remark(jumla)
        
        pdf.cell(40, 6, sub.upper(), 1)
        pdf.cell(20, 6, str(int(mazoezi_score)), 1, 0, "C")
        pdf.cell(20, 6, str(int(mitihani_score)), 1, 0, "C")
        pdf.cell(20, 6, str(int(jumla)), 1, 0, "C")
        pdf.cell(15, 6, grade, 1, 0, "C")
        
        pdf.set_font("Arial", "", 7.5)  # Drop font slightly for longer text remarks
        pdf.cell(60, 6, remark, 1)
        pdf.set_font("Arial", "", 9)
        
        pdf.cell(15, 6, "✔", 1, 1, "C")
        
    # Bottom Layout Cards
    pdf.ln(4)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(190, 4, "A(75-100) Bora  B(65-74) Vizuri  C(45-64) Amefaulu  D(30-44) Inaridhisha  F(0-29) Feli", ln=1, align="C")
    pdf.ln(4)
    
    # Statistical Summary Row
    pdf.set_font("Arial", "B", 9)
    pdf.cell(190, 5, f"JUMLA YA ALAMA: {int(student_row['total_all'])}  |  WASTANI: {student_row['final_average']:.1f}  |  NAFASI: {int(student_row['rank'])} Kati ya {total_students}", ln=1, align="L")
    pdf.ln(5)
    
    # Headmaster Custom Suggestions Box
    pdf.set_font("Arial", "B", 9)
    head_comment = get_headteacher_remark(student_row['final_average'])
    pdf.cell(190, 4, text=head_comment, ln=1, align="L")
    pdf.ln(4)
    
    pdf.set_font("Arial", "B", 8) 
    pdf.cell(190, 4, text="Saini ya Mkuu wa Shule: _______________________          MARTINE G. MAHEGA", ln=1, align="L")
    
    # Output file pipeline
    safe_name = "".join(x for x in str(student_row['name']) if x.isalnum() or x in "._- ")
    pdf.output(f"Taarifa_{safe_name}.pdf")

# --- 4. EXCEL DATA INTEGRATION PIPELINE ---
def process_data_and_run():
    conn = init_db()
    
    # Step A: Load the two separate source documents 
    try:
        df_mazoezi = pd.read_excel("Mid term results.xlsx") # Continuous tasks sheet
        df_mitihani = pd.read_excel("Stuents results.xlsx") # Term exam sheet
    except FileNotFoundError as e:
        print(f"❌ Excel File Missing: {e}")
        print("Please check your file names exactly: 'Mid term results.xlsx' and 'Stuents results.xlsx'")
        return

    # Clean the primary target key 'name' across both dataframes
    df_mazoezi['name'] = df_mazoezi['name'].astype(str).str.strip().str.lower()
    df_mitihani['name'] = df_mitihani['name'].astype(str).str.strip().str.lower()

    # Identify shared subjects based on the spreadsheet columns (excluding Name)
    subjects = [col for col in df_mitihani.columns if col.lower() != 'name']
    
    # Rename columns to keep them separate before merging
    df_mazoezi = df_mazoezi.rename(columns={sub: f"{sub}_mazoezi" for sub in subjects})
    df_mitihani = df_mitihani.rename(columns={sub: f"{sub}_mitihani" for sub in subjects})
    
    # Step B: Merging both datasets on Name
    merged_df = pd.merge(df_mitihani, df_mazoezi, on='name', how='inner')
    
    if merged_df.empty:
        print("❌ Warning: Merged data is empty! Check if student names match exactly in both files.")
        return

    # Step C: Performing math transformations loops
    total_running_sums = []
    
    for idx, row in merged_df.iterrows():
        student_total = 0
        for sub in subjects:
            m_val = row.get(f"{sub}_mazoezi", 0)
            e_val = row.get(f"{sub}_mitihani", 0)
            if pd.isna(m_val): m_val = 0
            if pd.isna(e_val): e_val = 0
            student_total += (m_val + e_val)
        total_running_sums.append(student_total)
        
    merged_df['total_all'] = total_running_sums
    merged_df['final_average'] = merged_df['total_all'] / len(subjects)
    merged_df['rank'] = merged_df['total_all'].rank(ascending=False, method='min').astype(int)
    
    # Export cleanly structured info to sqlite DB
    merged_df[['name', 'total_all', 'final_average', 'rank']].to_sql("student_data", conn, if_exists="replace", index=False)
    
    # Step D: Spin up printing execution loop
    total_students = len(merged_df)
    for index, row in merged_df.iterrows():
        make_pdf(row, row['rank'], total_students, subjects)
        print(f"📄 Report generated for: {row['name'].title()}")
        
    conn.close()
    print("\n🎉 Process Finished! All student records calculated and report card PDFs are ready.")

# --- 5. SECURE LOGIN BARRIER SCREEN ---
print("=========================================")
print("  SCHOOL MANAGEMENT SYSTEM - LOGIN SCREEN")
print("=========================================")

ADMIN_USER = "proffesionalIT"
ADMIN_PASS = "begin@2026"

username = input("Enter Username: ")
password = input("Enter Password: ")

if username == ADMIN_USER and password == ADMIN_PASS:
    print("\n✅ Login Successful! Welcome back, Teacher.\n")
    process_data_and_run()
else:
    print("\n❌ Error: Invalid Username or Password. Access Denied.")
