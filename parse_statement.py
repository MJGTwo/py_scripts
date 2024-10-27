import re
import sys
from typing import List, Dict

def parse_billing_data(data: str) -> List[Dict]:
    """
    Parses raw billing data text and extracts transactions including cash-back information.
    
    Args:
        data (str): Raw billing data as a string.
    
    Returns:
        List[Dict]: List of parsed transactions as dictionaries.
    """
    # Updated pattern to treat percentage as cash-back percentage and value as cash-back amount
    pattern = re.compile(
        r"(?P<date>\d{2}/\d{2}/\d{4})\s+"               # Date
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
            transactions.append(match.groupdict())
    
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_statement.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Read file content
    raw_data = read_file(file_path)
    
    # Parse the billing data
    billing_transactions = parse_billing_data(raw_data)
    
    # Output the parsed transactions to the terminal
    for transaction in billing_transactions:
        print(transaction)

if __name__ == "__main__":
    main()
