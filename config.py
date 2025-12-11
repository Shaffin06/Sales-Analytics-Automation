import cx_Oracle

USER = "Shaffin"
PASSWORD = "shaffin"
DSN = "localhost:1521/XE"   # change to your TNS / host/service

def get_connection():
    return cx_Oracle.connect(user=USER, password=PASSWORD, dsn=DSN)
