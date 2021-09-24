import psycopg2
from config import config

def connect():
    conn = None
    try:
        # reads the connection parameters.
        params = config()

        # connects to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # creates a cursor
        cur = conn.cursor()

        return conn, cur


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None, None


def close(conn):
    if conn is not None:
        conn.close()
        print("Database connection closed.")
    

def execute(statement=""):
    if statement == "":
        print("Please enter a statement to execute.")
        return
    
    try:
        conn, cursor = connect()
        if conn is None or cursor is None:
            print("Accessing the database has failed. Please try again.")
            close(conn)
            return

    
        # Executes the statement
        cursor.execute(statement)
        # Gets the response and prints the result.
        result = cursor.fetchall()
        print(result)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return

    finally:
        close(conn)

def createdatabase():
    execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
        task_id serial PRIMARY KEY,
        task_name VARCHAR (255) NOT NULL,
        status BOOLEAN NOT NULL
        );
        """)
    print("Created a database for the task list.")

def showtasks():
    return


if __name__ == "__main__":
    inputt = ""
    while inputt != "exit":
        inputt = input("What would you like to do? ")
        if inputt.lower == "show todo":
            print("okay")
            execute("SELECT * FROM tasks WHERE status = FALSE")
        elif inputt.lower == "create database":
            createdatabase()
        

    print("End of program")
