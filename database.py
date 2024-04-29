import psycopg2

# Function to connect to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="password_manager",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(e)
        return None

# Function to create the passwords table in PostgreSQL
def create_table():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                        (id SERIAL PRIMARY KEY,
                        site TEXT NOT NULL,
                        password TEXT NOT NULL)''')
        conn.commit()
        conn.close()
        
# Function to retrieve the password based on the user's email
def retrieve_password(site):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT password FROM passwords WHERE site = %s''', (site,))
        password = cursor.fetchone()
        conn.close()
        if password:
            return password[0]  # Return the password
    return None  # Return None if email/password not found or connection fails

# Function to insert a new password record into PostgreSQL
def insert_password(site, password):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO passwords (site, password)
                        VALUES (%s, %s)''', (site, password))
        conn.commit()
        conn.close()

# Function to update an existing password record in PostgreSQL
def update_password(site, password):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE passwords
                        SET site = %s, password = %s
                        WHERE site = %s''', (site, password, site))
        conn.commit()
        conn.close()

# Function to delete a password record from PostgreSQL
def delete_password(site):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM passwords WHERE site = %s''', (site,))
        conn.commit()
        conn.close()
        
# Testing
# create_table()
# retrieve_password("example.com")
# insert_password("example.com", "user123", "password123")
# update_password("example.com", "newpassword456")
# delete_password("example.com")