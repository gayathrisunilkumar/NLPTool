import psycopg2

hostname = 'localhost'
username = 'gayathri'
database = 'testdb'
password = 'gayu123'


def do_query(conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * from department""")
        rows = cur.fetchall()
        print "\nQuery output:\n"
        print(rows)
    except psycopg2.OperationalError:
        print("Operational Error")


myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
do_query(myConnection)

myConnection.close()
