import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="disha jain29",
    database="interview_system"
)

cursor = conn.cursor()

def save_result(category, score, performance):

    query = """
    INSERT INTO interview_history
    (category, score, performance)
    VALUES (%s, %s, %s)
    """

    values = (category, score, performance)

    cursor.execute(query, values)

    conn.commit()

def get_history():

    cursor.execute("""
        SELECT category, score, performance
        FROM interview_history
        ORDER BY id DESC
    """)

    return cursor.fetchall()