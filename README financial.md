"""
Utility functions for financial processing system
Helpers for data validation, error handling, and logging
"""

import os
import sys
from datetime import datetime
import pandas as pd
from financial_config import EXPECTED_COLUMNS, ERRORS, SUCCESS_MESSAGES

class FinancialLogger:
    """Simple logging utility for pipeline events"""
    
    @staticmethod
    def log(message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    @staticmethod
    def error(message: str):
        FinancialLogger.log(message, "ERROR")
    
    @staticmethod
    def warning(message: str):
        FinancialLogger.log(message, "WARNING")
    
    @staticmethod
    def success(message: str):
        FinancialLogger.log(message, "SUCCESS")
    
    @staticmethod
    def info(message: str):
        FinancialLogger.log(message, "INFO")


class DataValidator:
    """Validate input data for financial processing"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> tuple[bool, str]:
        """
        Validate dataframe has required columns and data types
        Returns: (is_valid: bool, message: str)
        """
        # Check for required columns
        missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        # Validate numeric columns
        numeric_cols = ['quantity', 'unit_price', 'discount_pct']
        for col in numeric_cols:
            try:
                pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                return False, f"Column '{col}' contains non-numeric values: {str(e)}"
        
        # Check for null invoice IDs
        if df['invoice_id'].isnull().any():
            return False, "Some invoice_id values are null"
        
        # Check for duplicate invoice IDs
        if df['invoice_id'].duplicated().any():
            duplicates = df[df['invoice_id'].duplicated()]['invoice_id'].tolist()
            return False, f"Duplicate invoice IDs found: {duplicates}"
        
        return True, "Data validation passed"
    
    @staticmethod
    def validate_numeric(value, column_name: str) -> bool:
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            FinancialLogger.error(f"Invalid numeric value in {column_name}: {value}")
            return False


class FileManager:
    """Manage file operations"""
    
    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Check if file exists"""
        return os.path.isfile(filepath)
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Safely delete a file"""
        try:
            if FileManager.file_exists(filepath):
                os.remove(filepath)
                FinancialLogger.info(f"Deleted file: {filepath}")
                return True
        except Exception as e:
            FinancialLogger.error(f"Failed to delete {filepath}: {str(e)}")
        return False
    
    @staticmethod
    def get_output_filename(invoice_id: str, client_name: str) -> str:
        """Generate standardized output filename"""
        safe_client_name = client_name.replace(' ', '_').replace('/', '_')
        return f"Invoice_{invoice_id}_{safe_client_name}.pdf"
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                FinancialLogger.info(f"Created directory: {directory}")
            return True
        except Exception as e:
            FinancialLogger.error(f"Failed to create directory {directory}: {str(e)}")
            return False


class FinancialCalculator:
    """Calculate financial metrics"""
    
    @staticmethod
    def calculate_subtotal(quantity: float, unit_price: float) -> float:
        """Calculate subtotal: quantity × unit_price"""
        return quantity * unit_price
    
    @staticmethod
    def calculate_discount(subtotal: float, discount_pct: float) -> float:
        """Calculate discount amount"""
        if discount_pct is None or pd.isna(discount_pct):
            discount_pct = 0
        return subtotal * max(0, min(discount_pct, 1.0))  # Clamp 0-1
    
    @staticmethod
    def calculate_vat(amount: float, vat_rate: float = 0.15) -> float:
        """Calculate VAT tax"""
        return amount * vat_rate
    
    @staticmethod
    def calculate_total(subtotal: float, discount: float, vat: float) -> float:
        """Calculate total due"""
        return (subtotal - discount) + vat
    
    @staticmethod
    def validate_amounts(subtotal: float, discount: float, vat: float, total: float) -> bool:
        """Validate financial calculations"""
        calculated_total = (subtotal - discount) + vat
        tolerance = 0.01  # Allow 0.01 TZS rounding difference
        
        if abs(calculated_total - total) > tolerance:
            FinancialLogger.warning(
                f"Total mismatch: calculated={calculated_total}, provided={total}"
            )
            return False
        return True


class ReportGenerator:
    """Generate financial reports"""
    
    @staticmethod
    def summary_report(df: pd.DataFrame) -> str:
        """Generate summary statistics"""
        report = "\n" + "="*60 + "\n"
        report += "FINANCIAL PROCESSING SUMMARY\n"
        report += "="*60 + "\n"
        report += f"Total Transactions: {len(df)}\n"
        report += f"Total Subtotal: {df['subtotal'].sum():,.2f} TZS\n"
        report += f"Total Discounts: {df['discount_amount'].sum():,.2f} TZS\n"
        report += f"Total VAT: {df['vat_tax'].sum():,.2f} TZS\n"
        report += f"Total Due: {df['total_due'].sum():,.2f} TZS\n"
        report += "="*60 + "\n"
        return report


class DateTimeHelper:
    """Handle date/time operations"""
    
    @staticmethod
    def get_today_string() -> str:
        """Get today's date as YYYY-MM-DD string"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_payment_due_date(days: int = 14) -> str:
        """Calculate payment due date"""
        from datetime import timedelta
        due_date = datetime.now() + timedelta(days=days)
        return due_date.strftime("%Y-%m-%d")
