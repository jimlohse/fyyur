import psycopg2

from psycopg2.extensions import AsIs

conn = psycopg2.connect(
    host="localhost",
    database="fyyurdb",
    user="postgres",
    password="letmein")

try:
    cur = conn.cursor()

    cur.execute('DELETE FROM venue WHERE id=1')

    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()