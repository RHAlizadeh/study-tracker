import pandas as pd
import os

# File path for saving/loading tracker
TRACKER_FILE = 'konkoor_tracker.csv'

# Columns and subjects
columns = ['Date', 'Subject', 'Planned Hours', 'Actual Hours', 'Notes']
subjects = [
    'Logic Circuit', 'Computer Architecture', 'Data Structures', 
    'Discrete Math', 'Digital Electronics', 'Operating Systems', 
    'Algorithm Design', 'Theory of Languages', 'Database', 'Artificial Intelligence'
]

# Load existing tracker or create new
if os.path.exists(TRACKER_FILE):
    tracker = pd.read_csv(TRACKER_FILE, parse_dates=['Date'], dayfirst=True)
else:
    tracker = pd.DataFrame(columns=columns)

# Function to add a daily entry
def add_entry(date, subject, planned_hours, actual_hours, notes=''):
    global tracker
    if subject not in subjects:
        print(f'Warning: {subject} is not in predefined subjects list.')

    # keep it as datetime internally
    date = pd.to_datetime(date, dayfirst=True)

    new_entry = pd.DataFrame([{
        'Date': date,
        'Subject': subject,
        'Planned Hours': planned_hours,
        'Actual Hours': actual_hours,
        'Notes': notes
    }])
    tracker = pd.concat([tracker, new_entry], ignore_index=True)

    # save with dd/mm/yyyy format
    tracker.to_csv(TRACKER_FILE, index=False, date_format="%d/%m/%Y")

    print(f'Entry added and saved for {subject} on {date.strftime("%d/%m/%Y")}.')

# Function for weekly summary
def weekly_summary(start_date, end_date):
    start_date = pd.to_datetime(start_date, dayfirst=True)
    end_date = pd.to_datetime(end_date, dayfirst=True)
    week_df = tracker[(tracker['Date'] >= start_date) & (tracker['Date'] <= end_date)]
    summary = week_df.groupby('Subject').agg({'Planned Hours':'sum', 'Actual Hours':'sum'})
    summary['Difference'] = summary['Actual Hours'] - summary['Planned Hours']
    summary['Status'] = summary['Difference'].apply(lambda x: ' Ahead' if x>0 else ('⚠ Behind' if x<0 else 'On Track'))
    return summary

# Function for monthly summary
def monthly_summary(month_start, month_end):
    month_start = pd.to_datetime(month_start, dayfirst=True)
    month_end = pd.to_datetime(month_end, dayfirst=True)
    month_df = tracker[(tracker['Date'] >= month_start) & (tracker['Date'] <= month_end)]
    summary = month_df.groupby('Subject').agg({'Planned Hours':'sum', 'Actual Hours':'sum'})
    summary['Difference'] = summary['Actual Hours'] - summary['Planned Hours']
    summary['Status'] = summary['Difference'].apply(lambda x: ' Ahead' if x>0 else ('⚠ Behind' if x<0 else 'On Track'))
    return summary


# Example usage
# Example usage: add some entries and show summaries
if __name__ == "__main__":
    add_entry('14/09/2025', 'Logic Circuit', 3, 3, 'Completed exercises 1-5')
    add_entry('15/09/2025', 'Computer Architecture', 2, 2, 'Reviewed pipelines')
    add_entry('15/09/2025', 'Discrete Math', 1, 1, 'Reviewed logic gates')

    print("Weekly Summary:")
    print(weekly_summary('14/09/2025', '20/09/2025'))

    print("\nMonthly Summary:")
    print(monthly_summary('01/09/2025', '30/09/2025'))
