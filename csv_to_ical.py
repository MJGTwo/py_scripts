import csv
import argparse
from icalendar import Calendar, Event
from datetime import datetime
import pytz  # Optional: For timezone handling
import uuid  # For generating unique UIDs
import os
import sys

def parse_arguments():
    """
    Parses command-line arguments.
    
    Returns:
        args: Parsed arguments containing input CSV and optional output ICS file paths.
    """
    parser = argparse.ArgumentParser(
        description='Convert a CSV of calendar events to an iCalendar (.ics) file.'
    )
    parser.add_argument(
        'input_csv',
        type=str,
        help='Path to the input CSV file containing calendar events.'
    )
    parser.add_argument(
        'output_ics',
        type=str,
        nargs='?',
        default=None,
        help='(Optional) Path to the output .ics file. If not provided, the .ics file will be named based on the input CSV.'
    )
    return parser.parse_args()

def generate_output_filename(input_csv):
    """
    Generates the output .ics filename based on the input CSV filename.
    
    Args:
        input_csv (str): Path to the input CSV file.
    
    Returns:
        str: Generated output .ics file path.
    """
    base, _ = os.path.splitext(input_csv)
    return f"{base}.ics"

def read_events_from_csv(csv_file_path):
    """
    Reads events from the specified CSV file.
    
    Args:
        csv_file_path (str): Path to the input CSV file.
    
    Returns:
        list of dict: List containing event details as dictionaries.
    """
    events = []
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, quotechar='"', escapechar='\\')
            for row in reader:
                events.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{csv_file_path}': {e}")
        sys.exit(1)
    return events

def create_icalendar(events, timezone=None):
    """
    Creates an iCalendar object from a list of events.
    
    Args:
        events (list of dict): List containing event details.
        timezone (pytz.timezone, optional): Timezone to localize event times. Defaults to None.
    
    Returns:
        Calendar: An iCalendar object containing all events.
    """
    cal = Calendar()
    cal.add('prodid', '-//Friends of Chamber Music//FCM Events//EN')
    cal.add('version', '2.0')
    
    for event in events:
        ical_event = Event()
        
        # Combine date and time
        start_datetime_str = f"{event['Start Date']} {event['Start Time']}"
        end_datetime_str = f"{event['End Date']} {event['End Time']}"
        
        # Parse datetime with proper format
        try:
            start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
            
            # Optional: Assign timezone
            if timezone:
                start_datetime = timezone.localize(start_datetime)
                end_datetime = timezone.localize(end_datetime)
            
            ical_event.add('dtstart', start_datetime)
            ical_event.add('dtend', end_datetime)
        except ValueError as e:
            print(f"Error parsing dates for event '{event['Subject']}': {e}")
            continue  # Skip this event
        
        # Add other event details
        ical_event.add('summary', event['Subject'])
        ical_event.add('description', event['Description'])
        ical_event.add('location', event['Location'])
        
        # Generate a unique identifier
        ical_event.add('uid', f"{uuid.uuid4()}")
        
        cal.add_component(ical_event)
    
    return cal

def write_icalendar(cal, output_file_path):
    """
    Writes the iCalendar object to a .ics file.
    
    Args:
        cal (Calendar): The iCalendar object.
        output_file_path (str): Path to the output .ics file.
    """
    try:
        with open(output_file_path, 'wb') as f:
            f.write(cal.to_ical())
        print(f"iCalendar file has been created at '{output_file_path}'")
    except Exception as e:
        print(f"Error writing to '{output_file_path}': {e}")
        sys.exit(1)

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    input_csv = args.input_csv
    output_ics = args.output_ics if args.output_ics else generate_output_filename(input_csv)
    
    # Optional: Define timezone
    # Uncomment and set your timezone if needed
    # timezone = pytz.timezone('America/New_York')
    timezone = None  # Set to None if not using timezone localization
    
    # Read events from CSV
    events = read_events_from_csv(input_csv)
    
    if not events:
        print("No events found in the CSV file.")
        sys.exit(0)
    
    # Create iCalendar object
    cal = create_icalendar(events, timezone)
    
    # Write to .ics file
    write_icalendar(cal, output_ics)

if __name__ == '__main__':
    main()
