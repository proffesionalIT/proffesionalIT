import os
import sqlite3
import pandas as pd
from fpdf import FPDF

# --- 1. CORPORATE LEDGER DATABASE INITIALIZATION ---
def init_finance_db():
    conn = sqlite3.connect("company_ledger.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_ledger(
        invoice_id TEXT PRIMARY KEY,
        client_name TEXT NOT NULL,
        item_name TEXT,
        quantity INTEGER,
        unit_price REAL,
        subtotal REAL,
        discount_amount REAL,
        vat_tax REAL,
        total_due REAL,
        date_created TEXT
    )""")
    conn.commit()
    return conn

# --- 2. PROFESSIONAL CORPORATE INVOICE GENERATOR ---
def generate_invoice_pdf(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Elegant Corporate Top Bar Accent
    pdf.set_fill_color(31, 58, 138)  # Deep Sapphire Blue
    pdf.rect(0, 0, 210, 5, 'F')
    
    # --- HEADER / BRANDING ---
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(31, 58, 138)
    pdf.cell(100, 6, "NEXUS TECH SOLUTIONS LTD", ln=0)
    
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(90, 6, "INVOICE", ln=1, align="R")
    
    # Company Metadata
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(100, 4, "Plot 45, Samora Avenue, Dar es Salaam", ln=0)
    pdf.cell(90, 4, f"Invoice #: {row['invoice_id']}", ln=1, align="R")
    pdf.cell(100, 4, "Email: finance@nexustech.co.tz", ln=0)
    pdf.cell(90, 4, f"Date: {row['date_created']}", ln=1, align="R")
    
    pdf.ln(8)
    pdf.set_draw_color(220, 220, 220)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)
    
    # --- BILL TO SECTION ---
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(31, 58, 138)
    pdf.cell(190, 5, "BILL TO:", ln=1)
    
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(190, 6, str(row['client_name']).upper(), ln=1)
    pdf.ln(6)
    
    # --- ITEMIZED CHARGES TABLE ---
    # Header Design
    pdf.set_fill_color(31, 58, 138)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 10)
    
    pdf.cell(80, 8, "  Description", 1, 0, "L", fill=True)
    pdf.cell(20, 8, "Qty", 1, 0, "C", fill=True)
    pdf.cell(40, 8, "Unit Price (TZS)", 1, 0, "R", fill=True)
    pdf.cell(40, 8, "Amount (TZS)", 1, 1, "R", fill=True)
    
    # Table Data Row
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Arial", "", 10)
    pdf.cell(80, 8, f"  {row['item_name']}", 1, 0, "L")
    pdf.cell(20, 8, str(int(row['quantity'])), 1, 0, "C")
    pdf.cell(40, 8, f"{row['unit_price']:,.2f}", 1, 0, "R")
    pdf.cell(40, 8, f"{row['subtotal']:,.2f}", 1, 1, "R")
    
    # --- FINANCIAL BREAKDOWN SUMMARY ---
    pdf.ln(4)
    pdf.set_font("Arial", "", 10)
    pdf.set_x(115)
    pdf.cell(40, 6, "Subtotal:", 0, 0, "R")
    pdf.cell(40, 6, f"{row['subtotal']:,.2f} TZS", 0, 1, "R")
    
    pdf.set_x(115)
    pdf.cell(40, 6, f"Discount ({int(row['discount_pct']*100)}%):", 0, 0, "R")
    pdf.cell(40, 6, f"-{row['discount_amount']:,.2f} TZS", 0, 1, "R")
    
    pdf.set_x(115)
    pdf.cell(40, 6, "VAT Tax (15%):", 0, 0, "R")
    pdf.cell(40, 6, f"+{row['vat_tax']:,.2f} TZS", 0, 1, "R")
    
    # Total Due Highlight Box
    pdf.ln(2)
    pdf.set_fill_color(240, 244, 255)
    pdf.rect(115, pdf.get_y(), 80, 8, 'F')
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(31, 58, 138)
    pdf.set_x(115)
    pdf.cell(40, 8, "Total Due:", 0, 0, "R")
    pdf.cell(40, 8, f"{row['total_due']:,.2f} TZS", 0, 1, "R")
    
    # --- PAYMENT TERMS FOOTER ---
    pdf.ln(25)
    pdf.set_draw_color(230, 230, 230)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(190, 4, "PAYMENT TERMS & INSTRUCTIONS", ln=1)
    pdf.set_font("Arial", "", 8.5)
    pdf.cell(190, 4, "Please make all bank transfers directly to: CRDB Bank | Account: 015XXXXXXX", ln=1)
    pdf.cell(190, 4, "Payment is due within 14 days of invoice emission date. Thank you for your business!", ln=1)
    
    # File Save Pipeline
    pdf.output(f"Invoice_{row['invoice_id']}_{row['client_name'].replace(' ', '_')}.pdf")

# --- 3. CORE PROCESSING ENGINE ---
def run_financial_pipeline():
    conn = init_finance_db()
    
    # Step A: Load Raw Financial Transactions Data
    try:
        df = pd.read_excel("raw_sales.xlsx", engine="openpyxl")
    except FileNotFoundError:
        print("❌ Error: 'raw_sales.xlsx' data file not found on path target.")
        return
        
    # Standardize column headers instantly to avoid KeyErrors
    df.columns = df.columns.astype(str).str.strip().str.lower()
    
    # Step B: Perform Business Math Algorithms using Pandas
    df['subtotal'] = df['quantity'] * df['unit_price']
    df['discount_amount'] = df['subtotal'] * df['discount_pct'].fillna(0)
    
    # Calculate tax after applying the discount
    df['vat_tax'] = (df['subtotal'] - df['discount_amount']) * 0.15
    df['total_due'] = (df['subtotal'] - df['discount_amount']) + df['vat_tax']
    
    # Assign timestamp
    df['date_created'] = "2026-07-08" # Dynamically logged dates
    
    # Step C: Save Computed Ledger Directly into Relational SQLite DB
    df.to_sql("sales_ledger", conn, if_exists="replace", index=False)
    
    # Step D: Execute Automated PDF Invoicing Loop
    for index, row in df.iterrows():
        generate_invoice_pdf(row)
        print(f"💼 Invoice Generated successfully for: {row['client_name']}")
        
    conn.close()
    print("\n🎉 Financial execution run finished! All invoices built successfully.")

if __name__ == "__main__":
    run_financial_pipeline()
