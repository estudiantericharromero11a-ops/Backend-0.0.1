import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",           # O la IP de tu máquina local
        port="5432",               # Puerto donde corre PostgreSQL (por defecto es 5432)
        user="postgres",           # Usuario que configuraste en PostgreSQL
        password="jklm212rich17",  # La contraseña que pusiste en la instalación
        dbname="Database-CUL/CUC_0.0.1",     # El nombre de tu base de datos
        client_encoding='utf-8'
    )