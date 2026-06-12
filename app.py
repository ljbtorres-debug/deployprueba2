import os
import time
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# 1. Variables de entorno solicitadas por el examen
APP_NAME = os.environ.get("APP_NAME", "Mi Aplicación Flask")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "empresa")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "admin123")

def inicializar_base_de_datos():
    """Conecta a PostgreSQL, crea la tabla productos e inserta 5 registros iniciales si está vacía."""
    conexion = None
    # Intenta conectar hasta 5 veces en caso de que la BD tarde en arrancar
    for _ in range(5):
        try:
            conexion = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            break
        except psycopg2.OperationalError:
            time.sleep(2)
    
    if not conexion:
        print("No se pudo conectar a la base de datos para la inicialización.")
        return

    cursor = conexion.cursor()
    
    # Crear tabla 'productos' con los campos solicitados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            precio NUMERIC(10, 2) NOT NULL,
            stock INT NOT NULL
        );
    """)
    
    # Verificar si ya existen registros para no duplicarlos
    cursor.execute("SELECT COUNT(*) FROM productos;")
    count = cursor.fetchone()[0]
    
    # Insertar los 5 registros requeridos
    if count == 0:
        productos_iniciales = [
            ("Laptop Gamer", 1250.00, 15),
            ("Mouse Óptico", 25.50, 40),
            ("Teclado Mecánico", 65.00, 25),
            ("Monitor 24 pulgadas", 180.00, 10),
            ("Auriculares Inalámbricos", 45.99, 30)
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s);",
            productos_iniciales
        )
        conexion.commit()
        print("Base de datos inicializada con 5 productos.")
        
    cursor.close()
    conexion.close()

# Ejecutar la inicialización al levantar la app
inicializar_base_de_datos()

@app.route("/")
def inicio():
    estado_conexion = "Desconectado"
    info_bd = ""
    try:
        conexion = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        info_bd = cursor.fetchone()[0]
        estado_conexion = "Exitosa (Conectado)"
        cursor.close()
        conexion.close()
    except Exception as e:
        estado_conexion = f"Error: {str(e)}"

    return f"""
    <h1>Nombre de la aplicación: {APP_NAME}</h1>
    <h2>Versión actual: {APP_VERSION}</h2>
    <p><strong>Estado de conexión con PostgreSQL:</strong> {estado_conexion}</p>
    <p><small>{info_bd}</small></p>
    <br>
    <a href="/productos">Ir a la ruta de productos (/productos)</a>
    """

@app.route("/productos")
def listar_productos():
    try:
        conexion = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos;")
        filas = cursor.fetchall()
        
        productos = []
        for fila in filas:
            productos.append({
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3]
            })
            
        cursor.close()
        conexion.close()
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)