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
    conn.commit()
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

def search_contact(contact_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM contacts WHERE id = %s''', (contact_id,))
        contact = cursor.fetchone()
        if contact:
            print("Contact found:")
            print("ID:", contact[0])
            print("Name:", contact[1])
            print("Email:", contact[2])
            print("Phone:", contact[3])
        else:
            print("No contact found with the provided ID.")
    except psycopg2.Error as e:
        print("Error: Unable to search contact:", e)

def view_all_contacts(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM contacts''')
        contacts = cursor.fetchall()
        if contacts:
            print("All Contacts:")
            for contact in contacts:
                print("ID:", contact[0])
                print("Name:", contact[1])
                print("Email:", contact[2])
                print("Phone:", contact[3])
                print("------------")
        else:
            print("No contacts found.")
    except psycopg2.Error as e:
        print("Error: Unable to view contacts:", e)


if __name__ == '__main__':
    conn = create_rw_conn()
    def main():
        while True:
            print("\nChoose an action:")
            print("1. Insert contact")
            print("2. Update contact")
            print("3. Delete contact")
            print("4. Search contact")
            print("5. View all contacts")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                name = input("Enter the name of the contact: ")
                email = input("Enter the email of the contact: ")
                phone = input("Enter the phone number of the contact: ")
                insert_contact(name, email, phone)
            elif choice == "2":
                contact_id = input("Enter the ID of the contact to update: ")
                name = input("Enter the new name: ")
                email = input("Enter the new email: ")
                phone = input("Enter the new phone number: ")
                update_contact(contact_id, name, email, phone)
            elif choice == "3":
                contact_id = input("Enter the ID of the contact to delete: ")
                delete_contact(contact_id)
            elif choice == "4":
                contact_id = input("Enter the ID of the contact to search: ")
                search_contact(contact_id)
            elif choice == "5":
                view_all_contacts(conn)
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose a valid action.")
    #contact_name = input("Enter the name of the contact: ")
    # contact_id = input("To change info enter the id of the contact: ")
    # contact_id = int(input("Enter the ID of the contact to delete: "))
    # conn = create_rw_conn()
    # init_table()
    # insert_contact("Hrehory", "dvornjaga666@gmail.com", "5555557777")
    # fetch_contacts()
    # print_contact_info_by_name(contact_name)
    # new_name, new_phone, new_email = "Kot", "kot@kot.com", "123"
    # update_contact(2, 'Danil', 'danil_suts@gmail.com', '0966666666')
    # delete_contact(contact_id)
    main()
    conn.commit()
    conn.close()
