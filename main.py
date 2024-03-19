import null
import psycopg2


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def create_rw_conn():
    # pass along secrets to pyscopg2
    PORT = "5432"
    USER = "postgres"
    PASSWORD = "admin"
    DATABASE = "contact_book"
    HOST = "localhost"

    # create connection string
    conn = psycopg2.connect(host=HOST, port=PORT, user=USER,
                            database=DATABASE, password=PASSWORD)
    # print("Connection established")

    return conn


def init_table():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT)''')
    print("Table created successfully")
    cursor.close()


def insert_contact(name, email, phone):
    cursor = conn.cursor()
    contacts_data = [
        (name, email, phone)
    ]
    for contact in contacts_data:
        cursor.execute('''INSERT INTO contacts (name, email, phone)
                          VALUES (%s, %s, %s) RETURNING id''', contact)
        inserted_id = cursor.fetchone()[0]
        print("Inserted contact with id:", inserted_id)

    cursor.close()

def fetch_contacts():
    cursor = conn.cursor()
    cursor.execute('''SELECT * from contacts''')
    result = cursor.fetchall()
    for row in result:
        id = row[0]
        name = row[1]
        email = row[2]
        phone = row[3]
        print(f' Contact {id}: {name} - {email} - {phone}')
    cursor.close()

def print_contact_info_by_name(contact_name):
    cursor = conn.cursor()
    cursor.execute('''SELECT name, email, phone FROM contacts WHERE name = %s''', (contact_name,))
    contact_info = cursor.fetchone()
    if contact_info:
        print("Contact Information:",contact_info[0], contact_info[1], contact_info[2])

    else:
        print("Contact not found.")
    cursor.close

if __name__ == '__main__':
    contact_name = input("Enter the name of the contact: ")
    conn = create_rw_conn()
    # init_table()
    # insert_contact("Danyl", "danya_sutts@gmail.com", "5555555556")
    # fetch_contacts()
    # print_contact_info_by_name(contact_name)
    conn.commit()
    conn.close()
