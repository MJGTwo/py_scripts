import re
import sys
import argparse
from typing import List, Dict

def convert_date_to_iso(date: str) -> str:
    """
    Converts a date from MM/DD/YYYY to YYYY-MM-DD using string manipulation.
    
    Args:
        date (str): Date in MM/DD/YYYY format.
    
    Returns:
        str: Date in YYYY-MM-DD format.
    """
    month, day, year = date.split('/')
    return f"{year}-{month}-{day}"

def parse_billing_data(data: str) -> List[Dict]:
    """
    Parses raw billing data text and extracts transactions including cash-back information,
    converting dates to ISO 8601 format using string manipulation.
    
    Args:
        data (str): Raw billing data as a string.
    
    Returns:
        List[Dict]: List of parsed transactions as dictionaries.
    """
    # Updated pattern to treat percentage as cash-back percentage and value as cash-back amount
    pattern = re.compile(
        r"(?P<date>\d{2}/\d{2}/\d{4})\s+"               # Date in MM/DD/YYYY format
        r"(?P<description>.+?)\s+"                      # Description (allow flexibility)
        r"(?P<cashback_percentage>-?\d+%)\s+"           # Cash-back percentage (can be negative)
        r"\$(?P<cashback_amount>-?[\d\.]+)\s+"          # Cash-back amount (can be negative)
        r"\$(?P<total>-?[\d\.]+)"                       # Total transaction amount (can be negative)
    )
    
    transactions = []
    
    lines = data.strip().split("\n")
    
    for line in lines:
        match = pattern.match(line)
        if match:
            transaction = match.groupdict()
            
            # Convert the date using string manipulation
            transaction['date'] = convert_date_to_iso(transaction['date'])
            
            transactions.append(transaction)
    
    return transactions

def read_file(file_path: str) -> str:
    """
    Reads the raw text file and returns its contents.
    
    Args:
        file_path (str): Path to the file to be read.
    
    Returns:
        str: Contents of the file as a string.
    """
    with open(file_path, 'r') as file:
        return file.read()

def parse_multiple_files(file_paths: List[str]) -> List[Dict]:
    """
    Parses multiple files and returns the combined list of transactions.
    
    Args:
        file_paths (List[str]): List of file paths to be read and parsed.
    
    Returns:
        List[Dict]: Combined list of parsed transactions.
    """
    all_transactions = []
    
    for file_path in file_paths:
        raw_data = read_file(file_path)
        transactions = parse_billing_data(raw_data)
        all_transactions.extend(transactions)
    
    return all_transactions

def main():
    parser = argparse.ArgumentParser(description="Parse billing statement files.")
    
    # Add a CLI argument for multiple file inputs
    parser.add_argument(
        '-f', '--files', 
        nargs='+', 
        required=True, 
        help="List of statement files to process."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Parse the files and collect all transactions
    all_transactions = parse_multiple_files(args.files)
    
    # Output the parsed transactions to the terminal
    for transaction in all_transactions:
        print(transaction)

if __name__ == "__main__":
    main()
