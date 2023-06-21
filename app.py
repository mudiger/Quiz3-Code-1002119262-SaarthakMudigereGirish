from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os
import redis
import time


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

driver = '{ODBC Driver 17 for SQL Server}'
server = 'sqlserver-1002119262-saarthakmudigeregirish.database.windows.net'
database = 'DataBase-1002119262-SaarthakMudigereGirish'
username = 'saarthakmudigeregirish'
password = 'Hello123'

# Establish the connection
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Create a cursor object
cursor = conn.cursor()

# Redis connection details
redis_host = 'Redis-1002119262-SaarthakMudigereGirish.redis.cache.windows.net'
redis_port = 6379
redis_password = 'My2SymFLIM78MdHnE61sCcWkM6G0HGWd6AzCaKwIZUU='

# Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
# redis_client.flushall()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page1/", methods=['GET', 'POST'])
def page1():
    total_time = []
    salpics = []
    if request.method == "POST":
        min = request.form['min']
        max = request.form['max']

        query = "SELECT City, State, Rank, Population FROM dbo.all_month WHERE Rank BETWEEN ? AND ?"
        start = time.time()
        cursor.execute(query, min, max)
        end = time.time()
        diff = end - start
        total_time.append(diff)

        row = cursor.fetchall()
        for i in row:
            salpics.append(i)

    return render_template("1)Page.html", salpics=salpics, total_time=total_time)


@app.route("/page2/", methods=['GET', 'POST'])
def page2():
    instance_time = []
    instance = []
    total_time = []
    salpics = []
    if request.method == "POST":
        num = request.form['num']
        min = request.form['min']
        max = request.form['max']

        for i in range(num):
            instance.append(i + 1)

        query = "SELECT City, State, Rank, Population FROM dbo.all_month WHERE Rank BETWEEN ? AND ?"
        s = time.time()
        for i in instance:
            start = time.time()
            cursor.execute(query, min, max)
            end = time.time()
            diff = end - start
            instance_time.append(diff)

            row = cursor.fetchall()
            for i in row:
                salpics.append(i)
        e = time.time()
        total_time.append(e - s)

    return render_template("2)Page.html", total_time=total_time, instance_time=instance_time, instance=instance, salpics=salpics)


@app.route("/page3/", methods=['GET', 'POST'])
def page3():
    instance_time = []
    instance = []
    total_time = []
    salpics = []
    redis_time = []

    if request.method == "POST":
        num = request.form['num']
        min = request.form['min']
        max = request.form['max']

        for i in range(num):
            instance.append(i + 1)

        query = "SELECT City, State, Rank, Population FROM dbo.all_month WHERE Rank BETWEEN ? AND ?"
        for i in instance:
            start = time.time()
            cursor.execute(query, min, max)
            end = time.time()
            instance_time.append(end-start)

            rows = cursor.fetchall()
            temp_result = ""
            for j in rows:
                temp_result = temp_result + str(j)
                salpics.append(i)

            redis_client.set(i, temp_result)
            s = time.time()
            temp = redis_client.get(i)
            e = time.time()
            redis_time.append(e - s)

    return render_template("3)Page.html", total_time=total_time, instance_time=instance_time, instance=instance, salpics=salpics)


if __name__ == "__main__":
    app.run(debug=True)