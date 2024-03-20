import null
import re
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
        validate_contact_data(email, phone)
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
    cursor.close()

def update_contact(contact_id, name, email, phone):
   task = """UPDATE contacts SET name = %s, email = %s, phone = %s
    WHERE id = %s"""
   data = (name, email, phone, contact_id)
   validate_contact_data(email, phone)
   update_database(task, data)

def delete_contact(contact_id):
    task = '''DELETE FROM contacts WHERE id = %s'''
    data = (contact_id,)
    update_database(task, data)

def update_database(task, data):
    cursor = conn.cursor()
    cursor.execute(task, data)
    conn.commit()
    cursor.close()


def validate_contact_data(email, phone):
    if not re.match(r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$', email):
        raise ValueError("Invalid email format")

    if not re.match(r'^\d{10}$', phone):
        raise ValueError("Invalid phone number format")


if __name__ == '__main__':
    #contact_name = input("Enter the name of the contact: ")
    # contact_id = input("To change info enter the id of the contact: ")
    # contact_id = int(input("Enter the ID of the contact to delete: "))
    conn = create_rw_conn()
    # init_table()
    # insert_contact("Hrehory", "dvornjaga666@gmail.com", "5555557777")
    # fetch_contacts()
    # print_contact_info_by_name(contact_name)
    # new_name, new_phone, new_email = "Kot", "kot@kot.com", "123"
    # update_contact(2, 'Danil', 'danil_suts@gmail.com', '0966666666')
    # delete_contact(contact_id)

    conn.commit()
    conn.close()
