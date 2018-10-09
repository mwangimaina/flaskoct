from flask import Flask, render_template, flash , session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/>?@$'

# every function is connected to a route
# we use the route to access the function
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/order/food')
def order():
    return 'I need to make some order'

@app.route('/comments')
def comments():
    return 'some nice comment.'

@app.route('/home')
def home():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('home.html')


# define route for products and return its template
@app.route('/products')
def products():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('products.html')

# define route for products and return its template
@app.route('/services')
def services():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('services.html')

# define route for products and return its template
@app.route('/join')
def join():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('join.html')


# define route for products and return its template
@app.route('/index')
def index():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('index.html')



# define route for products and return its template
@app.route('/index2')
def index2():
    # we need to create a HTML page for this route
    #in templates folder
    return render_template('index2.html')

import pymysql
# Application Layer - Logic
from flask import request
@app.route("/blog", methods=['POST','GET'])
def blog():
   # Logic goes here
   # handle form data
   if request.method=='POST':  # check if user posted something
       email = request.form['email']
       name = request.form['name']
       message = request.form['message']

       # validate fields
       if email=="":
           #flash("Email is Empty!")
           return render_template('blog.html', msg1="Email is Empty!")

       elif name =="":
            #flash("Name is Empty!")
            return render_template('blog.html', msg2="Name is Empty!")

       elif message=="":
           #flash("Message is Empty!")
           return render_template('blog.html', msg3="Message is Empty!")

       elif len(message)< 10:
           #flash("Message too Short")
           return render_template('blog.html', msg3="Too short")

       else:
           con = pymysql.connect("localhost","root","","mod_db")
           cursor = con.cursor()
           sql  = "INSERT INTO `messages_tbl`(`name`,`email`,`message`)VALUES(%s,%s,%s)"
           try:
              cursor.execute(sql,(name,email,message))
              con.commit() # commit changes to db
              return render_template('blog.html', msg="Uploaded!")
           except:
               con.rollback()
               return render_template('blog.html', msg="Failed!")

   else:
       return render_template('blog.html')
       # END


# create a table named register_tbl
# columns: username, password, firstname, lastname

# create a route/html save to DB
# =============VIEW ALL MESSAGES===========
@app.route("/blogs")
def blogs():
    if 'userkey' in session:
        # get the key value
        # no post required, we are only pulling all records
        # connect to db
        con = pymysql.connect("localhost", "root", "", "mod_db")

        # create cursor to execute SQL
        cursor = con.cursor()

        sql = "SELECT * FROM `messages_tbl` ORDER BY `reg_date` DESC"
        # execute SQL
        cursor.execute(sql)
        # count the returned rows
        if cursor.rowcount < 1:
            return render_template('blogs.html', msg= "No Messages Found")
        else:
            rows = cursor.fetchall()
            # send the rows to presentation Layer, your HTML
            return render_template('blogs.html', rows=rows)

    elif 'userkey' not in session:
        return redirect('/login')
    else:
        return redirect('/login')
# todo:


# searching from the database
@app.route("/search", methods=['POST','GET'])
def search():
    if request.method =='POST':
        name = request.form['name']
        con = pymysql.connect("localhost", "root", "", "mod_db")
        cursor = con.cursor()
        # do SQL
        sql = "SELECT * FROM `messages_tbl` WHERE `name`=%s ORDER BY `reg_date` DESC"
        cursor.execute(sql,(name))
        # check if cursor has zero rows
        if cursor.rowcount==0:
            return render_template('search.html', msg="No Messages Available")
        else:
            rows = cursor.fetchall()
            return render_template('search.html', rows=rows)

    else:
        return render_template('search.html')
        # Above function recieves a name from  the form  searches based
        # on the name , returns rows

con = pymysql.connect("localhost", "root", "", "mod_db")
cursor = con.cursor()
# searching from the database
@app.route("/customers", methods=['POST','GET'])
def customers():
    if 'userkey' in session:
        if request.method =='POST':
            Education = request.form['Education']
            # do SQL
            sql = "SELECT * FROM `customers` WHERE `Education`=%s"
            cursor.execute(sql,(Education))
            # check if cursor has zero rows
            if cursor.rowcount==0:
                return render_template('customers.html', msg="No Messages Available")
            else:
                rows = cursor.fetchall()
                return render_template('customers.html', rows=rows)
        else:
            sql = "SELECT * FROM `customers`"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return render_template('customers.html', rows=rows)

    elif 'userkey' not in session:
        return redirect('/login')
    else:
        return redirect('/login')






# delete blog route: this route receives a message_id
from flask import redirect
@app.route('/deleteblog/<msg_id>')
def deleteblog(msg_id):
    # we now delete the message with that id
    con = pymysql.connect("localhost", "root", "", "mod_db")
    cursor = con.cursor()
    sql = "DELETE FROM  messages_tbl WHERE message_id = %s "
    # execute sql, provide msg_id that we received
    try:
        cursor.execute(sql,(msg_id))
        con.commit()
        # check if cursor has zero rows
        return redirect('/search')  # route to search
    except:
        con.rollback()
        return redirect('/search')  # route to search


@app.route('/deletecustomer/<msg_id>')
def deletecustomers(msg_id):
    # we now delete the message with that id
    con = pymysql.connect("localhost", "root", "", "mod_db")
    cursor = con.cursor()
    sql = "DELETE FROM  customers WHERE `Name` = %s "
    # execute sql, provide msg_id that we received
    try:
        cursor.execute(sql,(msg_id))
        con.commit()
        # check if cursor has zero rows
        sql = "SELECT * FROM `customers` "
        cursor.execute(sql)
        rows = cursor.fetchall()
        return render_template('customers.html', msg2="Deleted : "+msg_id,rows=rows) # route to search
    except:
        con.rollback()
        return redirect('/search')  # route to search

# Login  Route
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        # connect to db
        con = pymysql.connect("localhost", "root", "", "mod_db")
        cursor = con.cursor()
        sql = "SELECT * FROM register_tbl WHERE username = %s AND password=%s"
        # execute SQL using the cursor
        cursor.execute(sql,(username,password))
        # check if a match was found/or not
        if cursor.rowcount==0:  # no user found
            return render_template('login.html', msg = "No Match. Wrong Input")
        elif cursor.rowcount==1: # 1 user found
           # create a session for the logged in
           # we store username in session variable
            session['userkey'] = username
            return redirect('/blogs')
        elif cursor.rowcount > 1:  # more than 1 user found
            return render_template('login.html', msg="Try Again Later")
        else:
            return render_template('login.html', msg="Contact Admin")
    else:  # shows login page,, after the route is visited
        return render_template('login.html')






#=============logout=============
@app.route('/logout')
def logout():
    session.pop('userkey',None)
    return redirect('/login')


#  Data Science
import pandas
import matplotlib.pyplot as plt
@app.route('/analysis')
def analysis():
    con = pymysql.connect("localhost", "root", "", "mod_db")
    dataframe = pandas.read_sql("SELECT MonthlyPremium, LastClaim, TotalClaim FROM customers", con)
    years = [2010,2012,2014,2015,2016,2018,2020]
    budget =[20000,15000,50000,60000,78000,45000,10000]
    # plot
    #plot, bar, scatter,
    plt.bar(years, budget)
    plt.title = "School Budget Distribution / Yearly"
    plt.xlabel = "Years "
    plt.ylabel = "Expense in KES"
    plt.savefig("static/bar.png")
    plt.show()

    plt.scatter(years, budget)
    plt.title = "School Budget Distribution / Yearly"
    plt.xlabel = "Years "
    plt.ylabel = "Expense in KES"
    plt.savefig("static/scatter.png")
    plt.show()

    return render_template('analysis.html')















#http://127.0.0.1:5000/blog
if __name__ == '__main__':
    app.run()
