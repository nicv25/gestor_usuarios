import mysql.connector


def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestor_usuarios"
    )

    if conn.is_connected(): 
        print("Conexion exitosa a la base de datos")
        
    return conn

        
conectar_bd()