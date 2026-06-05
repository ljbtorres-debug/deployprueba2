FROM python:3.14.5-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app

EXPOSE 5001
CMD [ "python","app.py" ]