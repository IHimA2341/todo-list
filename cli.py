import psycopg2
from config import config

def connect():
    conn = None
    try:
        # reads the connection parameters.
        params = config()

        # connects to the PostgreSQL server.
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

    
        # Executes the statement.
        cursor.execute(statement)
        # Gets the response and prints the result.
        result = cursor.fetchall()
        return result

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return

    finally:
        conn.commit()
        close(conn)


# Functions for the dictionary.

# creates a new table called tasks.
def createTable():
    execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
        task_id serial PRIMARY KEY,
        task_name VARCHAR (255) NOT NULL,
        status BOOLEAN NOT NULL
        );
        """)
    print("Created a table for the task list.")

# formats the data from the SELECT statements.
def formatData(data):
    data_list = ""
    for line in data:
        data_list += line[0] + "\n"
    
    return data_list

# shows the list of tasks that need doing.
def showTodo():
    task_list = execute("SELECT taskname, status FROM tasks WHERE status = FALSE;")
    task_list = formatData(task_list)
    final_str = "Things to do:\n" + task_list 
    print(final_str)

# shows the list of tasks that are completed.
def showCompleted():
    task_list = execute("SELECT taskname, status FROM tasks WHERE status = TRUE;")
    task_list = formatData(task_list)
    final_str = "Tasks that have been completed:\n" + task_list
    print(final_str)

# shows the full list of tasks.
def showFullList():
    task_list = execute("SELECT taskname, status FROM tasks;")
    task_list = formatData(task_list)
    final_str = "Here are the full list of tasks:\n" + task_list
    print(final_str)

# adds a task to the list.
def addTask():
    task_name = input("What is the task name? ")
    execute("INSERT INTO tasks (taskname, status) VALUES ('{0}', FALSE);".format(task_name))

# complete a task.
def completeTask():
    task_name = input("What is the task name? ")
    execute("UPDATE tasks SET status = TRUE WHERE taskname = '{0}';".format(task_name))
    
# delete a task.
def deleteTask():
    task_name = input("What is the task name? ")
    execute("DELETE FROM tasks WHERE taskname = '{0}'".format(task_name))

# exits the program.
def exitProgram():
    print("Thank you for using this program.")
    exit()

# Action when operation is invalid.
def invalidOp():
    print("It seems your input wasn't recognised. Please try again.")

def performoperation(chosen_ops):
    
    ops = {
        "show todo": showTodo,
        "show completed": showCompleted,
        "create table": createTable,
        "show list": showFullList,
        "add task": addTask,
        "complete task": completeTask,
        "delete task": deleteTask,
        "exit": exitProgram
        }
    
    chosen_op_function = ops.get(chosen_ops, invalidOp)
    return chosen_op_function()
    
if __name__ == "__main__":
    inputt = ""
    
    while True:
        inputt = input("What would you like to do? ")
        performoperation(inputt)
