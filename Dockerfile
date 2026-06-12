#1 Paso imagen base
FROM python:3.13-alpine

#2 Crear el directorio de trabajo
WORKDIR /app

#3 Instalar dependencias del sistema para psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev

#4 Copiar las dependencias
COPY requirements.txt /app

#5 Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

#6 Copiar el todo hacia /directorio o .
COPY app.py /app

#7 Ejecutar en el puerto 5000
EXPOSE 5001

#8 Ejecutar la aplicacion
CMD ["python", "app.py"]