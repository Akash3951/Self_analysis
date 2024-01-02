from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import date

app = Flask(__name__)

# connecting flask app to database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='daily_progress_report'

mysql = MySQL(app)
 

#  function to insert data to DB
def insertData(arr):
    day=arr[0]
    date=arr[1]
    marks=arr[2]

     # creating a connection cursor
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO daily_marks VALUES(%s, %s, %s)''',(day, date, marks))
    mysql.connection.commit()
    cursor.close()
    return 


# function to fetch data from DB
def fetchData():
     # creating a connection cursor
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM daily_marks")
    data = cursor.fetchall()
    cursor.close()
    return data


# function to calculate current average    
def calcAvg():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT AVG(Marks) FROM daily_marks")
    data = cursor.fetchone()
    cursor.close()
    average = data[0]
    if not average:
        return 0
    return round(average)



@app.route('/')
def start():
    return render_template("index.html", curr_avg = calcAvg())

@app.route('/submit', methods=['POST', 'GET'])
def getMarks():
    # get data after the form submition
    inputDate = request.form.get('date')
    inputDate = inputDate if inputDate else date.today()

    morning = request.form.get('morning')
    morning = int(morning) if morning else 0

    afternoon = request.form.get('afternoon')
    afternoon = int(afternoon) if afternoon else 0

    evening = request.form.get('evening')
    evening = int(evening) if evening else 0


    # calculate the average
    average = (morning + afternoon + evening)//3

    # # if date is not received by the user 
    # if not inputDate:
    #     inputDate = date.today()

    insertData(['', inputDate, average])
    return "updated successfully"


@app.route('/result', methods=['POST', 'GET'])
def showResults():
    data = fetchData()

    headers=['Day', 'Date', 'Marks']
    # print(data)
    return render_template("result.html", headers=headers, data=data)


   


if __name__=="__main__":
    app.run(host="0.0.0.0")


