import sqlite3


def execute_query(path: str, query: str, *args) -> list:
    """
    Executes a query against the database
    :param path: the database path
    :param query: the query string
    :param args: the query arguments, if there are any
    :return: a list, usually populated only with a select query
    """

    # Open the connection to the database and create a cursor object
    con = sqlite3.connect(path)
    cur = con.cursor()

    # Execute the query
    cur.execute(query, *args)
    result = cur.fetchall()

    # Save (commit) the changes
    con.commit()

    # Close the connection once we are done
    con.close()

    # return the resulting list
    return result


def is_table_in_db(path: str, table_name: str) -> bool:
    """
    Checks if a table exists in the database
    :param path: the database path
    :param table_name: the name of the table to check for
    :return: True if the table exists, otherwise False
    """

    return table_name in get_tables(path)


def get_tables(path: str) -> list:
    """
    Gets all the tables in the database
    :param path: the database path
    :return: a list of tables
    """

    # Open the connection to the database and create a cursor object
    con = sqlite3.connect(path)
    cur = con.cursor()

    # Execute the query
    result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    # Close the connection
    con.close()

    # process and return
    for i in range(0, len(result)):
        # print("before: ", tables[i])
        result[i] = result[i][0]
        # print("after: ", tables[i])

    return result


def drop_table(path: str, table_name: str) -> bool:
    """
    Drops a given table from the database if it exists
    :param path: the database path
    :param table_name: the name of the table to drop
    :return: True if the table was dropped, otherwise False
    """

    # Open the connection to the database and create a cursor object
    con = sqlite3.connect(path)
    cur = con.cursor()

    # the drop query statement
    drop_statement = "DROP TABLE {}".format(table_name)

    # try to execute the query
    result = False
    try:
        result = cur.execute(drop_statement).fetchall()
        result = True
    except sqlite3.OperationalError as err:
        pass
        print("[DROP TABLE OperationalError: {}] ".format(err))

    # Close the connection
    con.close()

    return result


def create_table(path: str, table_name: str, params: str) -> bool:
    """
    Create a table given the name of the table
    :param path: the database path
    :param table_name: the name of the table
    :param params: parameters for creating a new table
    :return: True if the table was created, otherwise False
    """
    # Open the connection to the database and create a cursor object
    con = sqlite3.connect(path)
    cur = con.cursor()

    # execute a CREATE statement to create a table
    create_statement = "CREATE TABLE {0} ({1})".format(
        table_name,
        params
    )

    # try to execute the statement
    result = False
    try:
        cur.execute(create_statement)
        result = True
    except sqlite3.OperationalError as err:
        pass
        print("[CREATE QUIZ TABLE OperationalError: {}] ".format(err))

    # close the connection
    con.close()

    # return the resulting list
    return result


def clear_tables(path: str):
    """
    Clears all tables from the database
    :param path: the database path
    :return: None
    """
    # get all the tables in the database
    tables = get_tables(path)

    # execute a DROP TABLE statement to drop all tables
    for table in tables:
        try:
            drop_table(path, str(table))
        except sqlite3.OperationalError as err:
            pass
            print("[CLEAR TABLES OperationalError: {}]".format(err))


