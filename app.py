from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hola Mundo byron</title>

    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, Helvetica, sans-serif;
        }

        body{
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
        }

        .card{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            width: 400px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }

        h1{
            font-size: 3rem;
            margin-bottom: 15px;
        }

        p{
            color: #cbd5e1;
            margin-bottom: 25px;
            line-height: 1.5;
        }

        .button{
            display: inline-block;
            padding: 12px 24px;
            border-radius: 10px;
            background: #38bdf8;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: 0.3s;
        }

        .button:hover{
            background: #0ea5e9;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <div class="card">
        <h1>Hola byron ponle 10/h1>

        <p>
            Tu aplicación Flask está funcionando correctamente.
        </p>

        <a href="/" class="button">
            Recargar
        </a>
    </div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)