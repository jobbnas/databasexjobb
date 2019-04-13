from flask import Flask
from flask import Flask, jsonify,flash
from flask import request
from flaskext.mysql import MySQL
from flask import render_template
import json

from flask import Response
from flask_cors import CORS
from flask import request
import requests
from bs4 import BeautifulSoup
import re

basic = {'1.1': "Moores law", '1.2': "Computer organization"}
javaboken = {

    'Chapter 1':'Introduction to Computers, the Internet and Java',
    'Chapter 2': 'Introduction to Java Applications; Input/Output and Operators',
    'Chapter 3': 'Introduction to Classes, Objects, Methods and Strings',
    'Chapter 4': 'Control Statements: Part 1; Assignment, ++ and — Operators',
    'Chapter 5': 'Control Statements: Part 2; Logical Operators',
    'Chapter 6': 'Methods: A Deeper Look',
    'Chapter 7': 'Arrays and ArrayLists',
    'Chapter 8': 'Classes and Objects: A Deeper Look',
    'Chapter 9': 'Object-Oriented Programming: Inheritance',
    'Chapter 10': 'Object-Oriented Programming: Polymorphism and Interfaces',
    'Chapter 11': 'Exception Handling: A Deeper Look',
    'Chapter 12': 'GUI Components: Part 1',
    'Chapter 13': 'Graphics and Java 2D',
    'Chapter 14': 'Strings, Characters and Regular Expressions',
    'Chapter 15': 'Files, Streams and Object Serialization',
    'Chapter 16': 'Generic Collections',
    'Chapter 17': 'Java SE 8 Lambdas and Streams',
    'Chapter 18': 'Recursion',
    'Chapter 19': 'Searching, Sorting and Big O',
    'Chapter 20': 'Generic Classes and Methods',
    'Chapter 21': 'Custom Generic Data Structures',
    'Chapter 22': 'GUI Components: Part 2',
    'Chapter 23': 'Concurrency',
    'Chapter 24': 'Accessing Databases with JDBC',
    'Chapter 25': 'JavaFX GUI: Part 1'

}




javaBook = json.dumps(javaboken)



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'newuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty'
app.config['MYSQL_DATABASE_DB'] = 'gggg'
app.config['MYSQL_DATABASE_HOST'] = '92.32.45.159'
mysql.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/questions2')
def getQuestions2():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return Response(json.dumps(json_data, ensure_ascii=False), mimetype='application/json' )

@app.route('/questions')
def getQuestions():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    conn.close()
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))



    for x in json_data:
        json_data2 = []

        #TEST
        conn = mysql.connect()
        cursor = conn.cursor()
        idquestions=str(x['idquestions'])
        cursor.execute("SELECT * FROM answer WHERE answer.questions_idquestions="+idquestions)
        row_headers = [x[0] for x in cursor.description]
        questions = cursor.fetchall()


        ansr= {}

        for result in questions:
            json_data2.append(dict(zip(row_headers, result)))
        print("json2")
        print(json_data2)
        x['answers']=json_data2

        #TEST


    return Response(json.dumps(json_data, ensure_ascii=False), mimetype='application/json', )

    #return jsonify({'questions':questions})

@app.route("/answers/<string:question_id>", methods=['GET'])
def getAnswers(question_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM answer WHERE answer.questions_idquestions="+question_id)

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return json.dumps(json_data,ensure_ascii=False)


@app.route("/quizanswers/<string:quizID>", methods=["GET"])
def getQuizAnswers(quizID):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizanswers WHERE quizID="+quizID)

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()
    json_data = []
    for result in questions:
        json_data.append(dict(zip(row_headers, result)))

    conn.close()
    return Response(json.dumps(json_data,ensure_ascii=False),mimetype='application/json')



@app.route("/dashboard")
def getDashboard():
    return render_template('Dashboardtest.html')

@app.route("/getBookChapter/<string:chapterID>")
def getChapter(chapterID):


    return Response ((javaBook),mimetype='application/json' )

@app.route("/summary",methods=['POST'])
def getSummary():
    testAnser = request.form['test']

    oop = int(request.form['oop'])
    java = int(request.form['java'])
    poly = int(request.form['poly'])
    xception = int(request.form['overloading'])


    answersDataJava= []
    answersDataPoly = []
    answersDataOOP = []

    answers={'mvc':3,'Java':java,'OOP':oop,'Poly':poly}

    summary={'Object-Oriented Programming':answers['OOP']/10,'Java':answers['Java']/5,'Classes':3/10,'Polymorphism':answers['Poly']/10}

    print(answers['Java'])

    for key, value in summary.items():
        if value<0.5:
            for nyckel, vrd in javaboken.items():

                if key in vrd:

                    if key=="Java":
                        answersDataJava.append(vrd)
                    elif key=="Polymorphism":
                        answersDataPoly.append(vrd)
                    elif key =="Object-Oriented Programming":
                        answersDataOOP.append(vrd)

    summary['Book ' + key] = answersDataJava
    summary['BookChapters '+ "Polymorphism"] = answersDataPoly
    summary['OOPchapter'] = answersDataOOP








    return Response(json.dumps(summary), mimetype='application/json')

@app.route("/scrape/<string:keyword>")
def getScrape(keyword):
    headers = {'Accept-Encoding': 'identity'}
    test=requests.get("https://www.tutorialspoint.com/java/",headers=headers)

    oracle=requests.get("https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html",headers=headers)

    w3 = requests.get("https://www.w3schools.com/java/",headers=headers)

    htmlW3 = BeautifulSoup(w3.content, 'html.parser')



    jsonW3 = []

    html = BeautifulSoup(test.content, 'html.parser')

    htmlOracle = BeautifulSoup(oracle.content, 'html.parser')



    for linkd in htmlW3.find_all("a", href=re.compile(keyword.lower())):
        links="https://www.w3schools.com/java/"+linkd.get("href")
        jsonW3.append(links)
    jsonOracle =[]


    for li in htmlOracle.find_all("a", href=re.compile(keyword)):

        links ="https://docs.oracle.com/javase/7/docs/api"+li.get("href")
        jsonOracle.append(links)




    jsonLink = []


    for link in html.find_all("a",href=re.compile(keyword.lower())):



        wholeLink = "https://www.tutorialspoint.com"+link.get("href")

        jsonLink.append(wholeLink)


    geeks = requests.get("https://www.geeksforgeeks.org/java/")

    htmlGeeks = BeautifulSoup(geeks.content,'html.parser')
    jsonGeeks = []

    for lins in htmlGeeks.find_all("a", href=re.compile(keyword)):

        linkG = "https://www.geeksforgeeks.org/java/"+lins.get("href")
        jsonGeeks.append(linkG)

    book = json.loads(javaBook)
    bookJson = []
    for x in range(1,25):

        chapter=book['Chapter '+str(x)]

        if keyword in chapter:
            bookJson.append(chapter)


    return jsonify({'Links':jsonLink,'OracleLinks':jsonOracle,"W3Links":jsonW3,"GeeksLinks":jsonGeeks,"Book":bookJson})

@app.route("/createuser/<string:nameID>", methods=['POST'])
def createUser(nameID):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO `user` (`name`) VALUES"+"("+"'"+nameID+"'"+");")
    conn.commit()
    conn.close()

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT max(iduser) from user")
    row_headers = [x[0] for x in cursor.description]

    userid=cursor.fetchall()
    conn.close()

    json_data = []

    for result in userid:
        json_data.append(dict(zip(row_headers, result)))


    return Response(json.dumps(json_data, ensure_ascii=False), mimetype='application/json')













@app.route("/getUser/<string:u_id>")
def getUser(u_id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE iduser="+u_id)

    row_headers = [x[0] for x in cursor.description]

    questions = cursor.fetchall()

    json_data = []

    for result in questions:
        json_data.append(dict(zip(row_headers, result)))


    conn.close()
    len(json_data)

    return json.dumps(json_data,ensure_ascii=False)







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
