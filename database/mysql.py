import mysql.connector
from app.config import MYSQL_CONFIG

def run_query(query):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur = conn.cursor()
    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    return res