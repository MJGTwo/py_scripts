import re
import sys
from typing import List, Dict

def parse_billing_data(data: str) -> List[Dict]:
    # Simplified pattern to extract key billing information without focusing on complex address parsing
    pattern = re.compile(
        r"(?P<date>\d{2}/\d{2}/\d{4})\s+"               # Date
        r"(?P<description>.+?)\s+"                      # Description (allow flexibility)
        r"(?P<percentage>\d+%)\s+"                      # Percentage
        r"\$(?P<tax>[\d\.]+)\s+"                        # Tax
        r"\$(?P<total>[\d\.]+)"                         # Total
    )
    
    transactions = []
    
    # Split the input data into lines
    lines = data.strip().split("\n")
    
    for line in lines:
        match = pattern.match(line)
        if match:
            transactions.append(match.groupdict())
    
    return transactions

def read_file(file_path: str) -> str:
    """Reads the raw text file and returns its contents."""
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
