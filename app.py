from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3


app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists customer(pid integer primary key,name text,address text,contact integer,mail text,mode text,exam text,marks text)")
con.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        if((name == "admin") and password == ("admin")):
            return redirect("admin_register")
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and mail=? and mode='stu'",(name,password))
        data=cur.fetchone()
        cur.execute("select * from customer where name=? and mail=? and mode='fac'",(name,password))
        data1 = cur.fetchone()
        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("customer")
        if data1:
            return redirect("teacher")
        else:
            flash("Username and password does not match","error")
    return redirect(url_for("index"))


@app.route('/customer',methods=["GET","POST"])
def customer():
    con=sqlite3.connect("database.db")
    cur=con.cursor()
    cur.execute("select marks from customer where name = 'student'")
    mark = cur.fetchall()[0]
    for i in mark:
        markss = i
    con.commit()
    cur.execute("select exam from customer where name = 'student'")
    exam = cur.fetchall()[0]
    for i in exam:
        examss = i
    con.commit()

    return render_template("customer.html",marks = markss,exam = examss)

@app.route('/teacher',methods=["GET","POST"])
def teacher():
    if request.method=='POST':
        try:
            exam=request.form['exam']
            stu=request.form['stu']
            marks=request.form['marks']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM customer WHERE name = ?;",(stu))
            cur.execute("UPDATE customer SET marks = ?;",(marks))
            con.commit()
            flash("Uploaded","success")
        except:
            flash("Error ","Failed")
        finally:
            con.close()

    return render_template('teacher.html')

@app.route('/admin_register',methods=['GET','POST'])
def admin_register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            mode = request.form.get("mode")
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into customer(name,address,contact,mail,mode)values(?,?,?,?,?)",(name,address,contact,mail,mode))
            con.commit()
            flash("Registered","success")
        except:
            flash("Error , data already present","Failed")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('admin_register.html')

@app.route('/forgor',methods=["GET","POST"])
def forgor():
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['key']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and contact=?",(name,contact))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("customer")

        else:
            flash("Username and password does not match","error")
    return render_template('forgor.html')



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            mode = 'stu'
            cur=con.cursor()
            cur.execute("insert into customer(name,address,contact,mail,mode)values(?,?,?,?,?)",(name,address,contact,mail,mode))
            con.commit()
            flash("Registered","success")
        except:
            flash("Error , data already present","Failed")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
