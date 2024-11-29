import pyodbc
from config.config import DB_CONFIG

def fetch_all_data():
    """Fetch all data from the database."""
    connection = None
    try:
        connection = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['uid']};"
            f"PWD={DB_CONFIG['pwd']}"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM applicants")
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows
    except pyodbc.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if connection:
            connection.close()

def fetch_paginated_data(page, per_page):
    """Fetch paginated data from the database."""
    connection = None
    offset = (page - 1) * per_page
    try:
        connection = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['uid']};"
            f"PWD={DB_CONFIG['pwd']}"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM applicants ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, offset, per_page)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows
    except pyodbc.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if connection:
            connection.close()

def fetch_applicant_by_id(doc_id):
    """Fetch a specific applicant's data by ID."""
    connection = None
    try:
        connection = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['uid']};"
            f"PWD={DB_CONFIG['pwd']}"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM applicants WHERE id = ?"
        cursor.execute(query, doc_id)
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        else:
            return None
    except pyodbc.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if connection:
            connection.close()
