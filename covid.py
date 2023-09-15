import sqlite3
from tabulate import tabulate

# Initialize an SQLite database
conn = sqlite3.connect('covid_data.db')
cursor = conn.cursor()

# Create a table to store survey responses if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS survey_responses (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        location TEXT,
        symptoms TEXT
    )
''')
conn.commit()

# Function to add a new survey response
def add_survey_response():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    location = input("Enter your location: ")
    symptoms = input("Enter your symptoms (comma-separated): ").split(',')

    response = {
        "Name": name,
        "Age": age,
        "Location": location,
        "Symptoms": symptoms
    }

    # Insert the response into the database
    cursor.execute('''
        INSERT INTO survey_responses (name, age, location, symptoms)
        VALUES (?, ?, ?, ?)
    ''', (name, age, location, ', '.join(symptoms)))

    conn.commit()

# Function to view data in a table format
def view_data_table():
    cursor.execute('SELECT name, age, location, symptoms FROM survey_responses')
    data = cursor.fetchall()

    if not data:
        print("No data available.")
        return

    headers = ["Name", "Age", "Location", "Symptoms"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

# Main program loop
while True:
    print("\nCOVID-19 Data Maintenance and Survey")
    print("1. Add Survey Response")
    print("2. View Survey Data (Table Format)")
    print("3. Exit")

    choice = input("Select an option: ")

    if choice == '1':
        add_survey_response()
    elif choice == '2':
        view_data_table()  # View data in table format
    elif choice == '3':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection when done
conn.close()
