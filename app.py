from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Variables de entorno con valores por defecto
APP_NAME = os.getenv("APP_NAME", "Tienda DevOps")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "database": os.getenv("DB_NAME", "tienda"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def inicio():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version_db = cursor.fetchone()
        cursor.close()
        conn.close()

        estado = "Conexión exitosa "
        color = "green"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{APP_NAME}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .card {{ border: 1px solid #ddd; padding: 20px; border-radius: 8px; max-width: 500px; }}
                h1 {{ color: #333; }}
                .version {{ color: #666; }}
                .estado {{ color: {color}; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>{APP_NAME}</h1>
                <p class="version">Versión: <b>{APP_VERSION}</b></p>
                <p class="estado">{estado}</p>
                <p><b>PostgreSQL:</b> {version_db[0]}</p>
                <hr>
                <p><a href="/productos">📦 Ver Productos</a></p>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h1>{APP_NAME}</h1>
        <p class="estado" style="color:red;">❌ Error de conexión: {str(e)}</p>
        """, 500

@app.route("/productos")
def listar_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos ORDER BY id;")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        filas = ""
        for p in productos:
            filas += f"<tr><td>{p[0]}</td><td>{p[1]}</td><td>${p[2]:.2f}</td><td>{p[3]}</td></tr>"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Productos - {APP_NAME}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                table {{ border-collapse: collapse; width: 60%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                a {{ color: #4CAF50; text-decoration: none; }}
            </style>
        </head>
        <body>
            <h1>📦 Lista de Productos</h1>
            <p class="version">Versión: <b>{APP_VERSION}</b></p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Precio</th>
                    <th>Stock</th>
                </tr>
                {filas}
            </table>
            <br>
            <a href="/"> Volver</a>
        </body>
        </html>
        """

    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)