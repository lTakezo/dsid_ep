from flask import Flask, redirect, url_for, render_template, request, jsonify, session
import subprocess, json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import apicaller


app = Flask(__name__)

app.secret_key = 'fts'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'T@wFpxLFo4pO'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)

@app.route("/")
def home():
    if "loggedin" in session:
        user = session["username"]
        return render_template("index.html", content=user, loggedin=True)
    
    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/profile/')
def profile(type=None, content=None):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account, loggedin=True, type=type, content=content)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/hotel/", methods=["POST", "GET"])
def hotel():
    try:
        if request.method == "POST" and request.form["dest"]:
            dest = request.form["dest"]
            hotel_params = []
            hotel_params.append(request.form["qt_ad"])
            hotel_params.append(request.form["checkin"])
            hotel_params.append(request.form["qt_qu"])
            hotel_params.append(request.form["qt_no"])
            hotel_params.append(request.form["pr_mx"])
            
            querylist = [dest, "Hoteis"]
            apicaller.set_localid(querylist)
            apijson = apicaller.queryhotels(hotel_params)

            results = [] # each restaurante will be a list inside this list
            for i in range(0, len(apijson['data'])):
                results_i = [] # name, latitude, longitude, photo, rating, price, address
                for k, v in apijson['data'][i].items():
                    if k == 'name':
                        results_i.append(v)
                    elif k == 'latitude':
                        results_i.append(v)
                    elif k == 'longitude':
                        results_i.append(v)
                    elif k == 'photo':
                        results_i.append(v['images']['small']['url'])
                    elif k == 'rating':
                        results_i.append(v)
                    elif k == 'price':
                        results_i.append(v)       
                results.append(results_i)

            if "loggedin" in session:
                return render_template("hotel_result.html", contents=results, dest=dest, loggedin=True)
            else:
                return render_template("hotel_result.html", contents=results, dest=dest)

    except:
        if request.method == "POST":

            data = request.form["content"].strip("']['").split("', '")

            return profile(type="Hotel", content=data)

    else:
        if "loggedin" in session:
            return render_template("hotel.html", loggedin=True)
        else:
            return render_template("hotel.html")


@app.route("/restaurante/", methods=["POST", "GET"])
def restaurante():
    try:
        if request.method == "POST" and request.form["dest"]:
            # Parametros
            dest = request.form["dest"] # tem que eliminar espaço do comeco e fim dos parametros
            pr_min = request.form["p_min"]
            pr_max = request.form["p_max"]
            querylist = [dest, "Restaurantes"]
            # query para API
            apicaller.set_localid(querylist)
            apijson = apicaller.queryrestaurant(pr_min + '%2C' + pr_max)

            results = [] # each restaurante will be a list inside this list
            for i in range(0, len(apijson['data'])):
                results_i = [] # name, photo, rating, description, phone, website, address
                for k, v in apijson['data'][i].items():
                    if k == 'name':
                        results_i.append(v)
                    elif k == 'photo':
                        results_i.append(v['images']['small']['url'])
                    elif k == 'rating':
                        results_i.append(v)
                    elif k == 'description':
                        results_i.append(v)
                    elif k == 'phone':
                        results_i.append(v)
                    elif k == 'website':
                        results_i.append(v)
                    elif k == 'address':
                        results_i.append(v)        
                results.append(results_i)
            if "loggedin" in session:
                return render_template("restaurante_result.html", contents=results, dest=dest, loggedin=True)
            else:
                return render_template("restaurante_result.html", contents=results, dest=dest)

    except:
        if request.method == "POST":

            data = request.form["content"].strip("']['").split("', '")
            #jsondata = "{'name':'"+data[0]+"', 'photo':'"+data[1]+"', 'phone':'"+data[4]+"', 'website':'"+data[5]+"', 'address':'"+data[6]+"'}"
            #print(request.form["content"])

            return profile(type="Restaurante", content=data)

    else:
        if "loggedin" in session:
            return render_template("restaurante.html", loggedin=True)
        else:
            return render_template("restaurante.html")

@app.route("/atracao/", methods=["POST", "GET"])
def atracao():
    try:
        if request.method == "POST" and request.form["dest"]:
            dest = request.form["dest"] # tem que eliminar espaço do comeco e fim dos parametros
            rate = request.form["rate"]
            querylist = [dest, "Atracoes"]
            apicaller.set_localid(querylist)
            apijson = apicaller.queryatractions(rate)

            results = [] # each restaurante will be a list inside this list
            for i in range(0, len(apijson['data'])):
                results_i = [] # name, photo, rating, desciption, address
                for k, v in apijson['data'][i].items():
                    if k == 'name':
                        results_i.append(v)
                    elif k == 'photo':
                        results_i.append(v['images']['small']['url'])
                    elif k == 'rating':
                        results_i.append(v)
                    elif k == 'description':
                        results_i.append(v)
                    elif k == 'address':
                        results_i.append(v)        
                results.append(results_i)

            if "loggedin" in session:
                return render_template("atracao_result.html", contents=results, dest=dest, loggedin=True)
            else:
                return render_template("atracao_result.html", contents=results, dest=dest)

    except:
        if request.method == "POST":

            data = request.form["content"].strip("']['").split("', '")

            return profile(type="Atração", content=data)

    else:
        if "loggedin" in session:
            return render_template("atracao.html", loggedin=True)
        else:
            return render_template("atracao.html")


if __name__ == "__main__":
    app.run(debug=True)