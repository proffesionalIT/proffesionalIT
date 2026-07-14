# School Management System - Student Report Card Generator

## Overview

`excel2.py` is a comprehensive **School Management System** that automates the process of generating student report cards in PDF format. It integrates data from multiple Excel spreadsheets, performs statistical calculations, assigns grades, and generates beautifully formatted report cards with teacher remarks and headmaster comments in **Swahili**.

**School:** Shule ya Sekondari Waangwaray  
**Language:** Swahili (with English support)  
**Output Format:** PDF Report Cards

---

## Features

✨ **Key Capabilities:**

- **Multi-Source Data Integration** - Merges continuous assessment (mazoezi) and exam (mitihani) scores from separate Excel files
- **Dynamic Grading System** - Automatically assigns letter grades (A-F) based on total scores
- **Intelligent Remarks** - Generates personalized Swahili remarks for each subject
- **Ranking System** - Calculates student rankings based on total marks
- **PDF Generation** - Creates professional report cards with school logos and formatted tables
- **Database Storage** - Stores processed data in SQLite for easy retrieval and analysis
- **Secure Login** - Admin authentication to prevent unauthorized access
- **Batch Processing** - Generates report cards for all students in one execution

---

## System Requirements

### Dependencies

```
pandas        - Data manipulation and Excel file reading
fpdf          - PDF generation and formatting
sqlite3       - Database operations (built-in)
openpyxl      - Excel file support (required by pandas)
```

### Installation

```bash
pip install pandas fpdf openpyxl
```

### Input Files Required

1. **Mid term results.xlsx** - Contains continuous assessment scores (mazoezi)
   - Column 1: `name` (student names)
   - Columns 2+: Subject names with continuous scores

2. **Stuents results.xlsx** - Contains exam scores (mitihani)
   - Column 1: `name` (student names - must match first file)
   - Columns 2+: Subject names with exam scores

### Optional Files

- `photo.jpg` - School logo/photo (left side of header)
- `image.jpg` - Ministry/organization logo (right side of header)

---

## How It Works

### 1. **Login Screen**
```
Username: proffesionalIT
Password: begin@2026
```

### 2. **Data Processing Pipeline**

```
Excel Files (Input)
    ↓
    └─→ Load both spreadsheets
    ↓
    └─→ Clean student names (lowercase, strip whitespace)
    ↓
    └─→ Identify shared subjects
    ↓
    └─→ Merge datasets on student name
    ↓
    └─→ Calculate totals and averages
    ↓
    └─→ Generate rankings
    ↓
    └─→ Store in SQLite database
    ↓
PDF Report Cards (Output)
```

### 3. **Grading System**

| Grade | Score Range | Swahili Remark |
|-------|-------------|----------------|
| **A** | 75-100 | Vizuri Sana (Excellent) |
| **B** | 65-74 | Vizuri (Very Good) |
| **C** | 45-64 | Amefaulu (Good) |
| **D** | 30-44 | Inaridhisha (Satisfactory) |
| **F** | 0-29 | Feli (Failed) |

### 4. **PDF Report Card Contents**

Each generated report includes:
- Student name and class (Kidato cha Pili)
- Term and year (Muhula wa II Mwaka 2026)
- Subject performance table with:
  - Continuous Assessment (Mazoezi)
  - Exam Scores (Mtihani)
  - Total marks
  - Grade
  - Teacher remarks
- Overall statistics:
  - Total marks
  - Average score
  - Class ranking
- Headmaster custom remarks based on performance
- Signature line

---

## Core Functions

### `init_db()`
Initializes SQLite database and creates `student_data` table with columns:
- `name`, `total_marks`, `average`, `division`, `rank`

### `get_grade_and_remark(score)`
Returns grade (A-F) and corresponding Swahili teacher remarks based on score.

### `get_headteacher_remark(average)`
Generates personalized headmaster comments based on final average:
- **75+:** Honors student for excellence
- **50-74:** Encourages improvement
- **<50:** Recommends additional support

### `make_pdf(student_row, rank, total_students, subject_list)`
Generates a formatted PDF report card for individual students with:
- Header with school logos and titles
- Subject performance table
- Grading scale reference
- Statistics and remarks
- Signature line

### `process_data_and_run()`
Main execution function that orchestrates the entire pipeline:
1. Initializes database
2. Loads Excel files
3. Merges and processes data
4. Calculates statistics
5. Generates PDFs for all students

---

## Usage

### Running the Program

```bash
python excel2.py
```

### Step-by-Step Execution

1. **Start the program** - Login screen appears
2. **Enter credentials** - Use provided username and password
3. **Place Excel files** - Ensure both required Excel files are in the same directory
4. **Run** - Press Enter to start processing
5. **Output** - PDF files generated as `Taarifa_{StudentName}.pdf`

### Example Output

```
✅ Login Successful! Welcome back, Teacher.

📄 Report generated for: John Doe
📄 Report generated for: Jane Smith
📄 Report generated for: Moses Kipchoge
...
🎉 Process Finished! All student records calculated and report card PDFs are ready.
```

---

## Database Schema

### `student_data` Table

| Column | Type | Description |
|--------|------|-------------|
| `name` | TEXT | Student name (normalized) |
| `total_all` | REAL | Sum of all subject marks |
| `final_average` | REAL | Average score across subjects |
| `rank` | INTEGER | Class ranking (1 = top) |

---

## Error Handling

### Common Issues & Solutions

**❌ "Excel File Missing"**
- Ensure both files exist in working directory
- Check exact filenames: `Mid term results.xlsx` and `Stuents results.xlsx`
- Note: There's a typo in the second filename ("Stuents" instead of "Students") - match this exactly

**❌ "Merged data is empty"**
- Student names must match exactly between both files
- Check for extra spaces, different capitalizations
- Ensure name column is labeled `name` in both files

**❌ "Invalid Username or Password"**
- Verify credentials: `proffesionalIT` / `begin@2026`
- Check for accidental spaces in input

---

## File Outputs

- **PDF Report Cards:** `Taarifa_{StudentName}.pdf`
- **Database:** `school.db` (SQLite)
- **Console Output:** Progress messages and completion summary

---

## Customization

### Modify Grading Thresholds

Edit the `get_grade_and_remark()` function:
```python
if score >= 75:  # Change to your threshold
    return "A", "Vizuri Sana (Excellent)..."
```

### Change School Information

Update these variables in `make_pdf()`:
```python
pdf.cell(190, 5, "YOUR_SCHOOL_NAME", ln=1, align="C")
pdf.cell(190, 5, "YOUR_FORM_LEVEL", ln=1, align="C")
```

### Add/Remove Subjects

Subjects are automatically detected from Excel column headers (excluding 'name').

---

## Security Notes

⚠️ **Important:**
- Hard-coded credentials are visible in source code - not recommended for production
- Consider using environment variables or configuration files
- Protect the `school.db` database file
- Backup reports before clearing

---

## Future Enhancements

- [ ] GUI login interface
- [ ] Configurable grading scales
- [ ] Multiple term support
- [ ] Email report delivery
- [ ] Student portal access
- [ ] Performance analytics dashboard
- [ ] Multi-language support

---

## Author

Created for Shule ya Sekondari Waangwaray School Management System

---

## License

Internal Use Only - School Administration

---

## Support

For issues or modifications, contact the system administrator.
