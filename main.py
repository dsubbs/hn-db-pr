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
    print("Connection established")

    return conn


def init_table():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT)''')
    print("Table created successfully")
    cursor.close()

if __name__ == '__main__':
    conn = create_rw_conn()
    init_table()
    conn.commit()
    conn.close()





