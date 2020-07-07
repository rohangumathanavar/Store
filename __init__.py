from flask import Flask, render_template, request, redirect, url_for,session,flash
from flaskext.mysql import MySQL
from functools import wraps
import mysql.connector
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

mysql.init_app(app)
mysql = MySQL(app)
conn = mysql.connect()
cur = conn.cursor()
#################################################### Session ############################################


################################################## MAIN  ################################################
@app.route('/', methods = ['GET' ,'POST'])
def index():
    return render_template('Main.html')
##########################################################################################################
@app.route('/sikttu/',methods = ['GET', 'POST'])
def sikttu():
    if request.method=="POST":
        user_details=request.form
        id=str(user_details['rol'])
        cur.execute("select uid,uname,phno from user where uname=%s",id)
        data=cur.fetchall()
        return render_template('sikttu.html',data=data)
    cur.execute("select * from user")
    data = cur.fetchall()
    return render_template('sikttu.html',data=data)



def getApp():
    return app
########################################################## Add to cart ############################################
@app.route('/addtocart/<id1>',methods = ['GET', 'POST'])
def addtocart(id1):
    if request.method == 'POST':
        user_details = request.form
        qty=str(user_details['qty'])
        pid=str(user_details['pid'])
        cur.execute("insert  into order1 (uid,pid,qty) values (%s,%s,%s);",(id1,pid,qty))
        conn.commit()
        mesg=pid+" is  added and quantity is "+qty
        cur.execute("select * from product;")
        data = cur.fetchall()
        return render_template('products.html',id=id1,data=data,mesg=mesg)
    #print(id+"  "+pid)
    cur.execute("select * from product;")
    data = cur.fetchall()
    return render_template('products.html',id=id1,data=data)
############################################################ delete quantity ##################################
@app.route('/delete/',methods = ['GET', 'POST'])
def delete():
    cur.execute("delete table order1;")
    conn.commit()
    return "quantity is deleted"
########################################################### User Info ##########################################
@app.route('/user_info/',methods = ['GET', 'POST'])
def user_info():
    cur.execute("select* from user;")
    data=cur.fetchall()
    return render_template("user_info.html",data=data)
########################################################## RAte Update #############################################
@app.route('/product_rate/<id>',methods = ['GET', 'POST'])
def product_rate(id):
    if request.method == 'POST':
        user_details = request.form
        pname=str(user_details['pname'])
        rate=str(user_details['rate'])
        try:
            cur.execute("update product set rate=%s,pname=%s where pid=%s;", (rate, pname, id))
            conn.commit()
            cur.execute("select * from product")
            data = cur.fetchall()
            return render_template("product_update.html", data=data)
        except:
            return "invalid product_name or rate"
    cur.execute("select pid from product where pid=%s;",id)
    data=cur.fetchone()
    cur.execute("select pname from product where pid=%s;", id)
    data1 = cur.fetchone()
    cur.execute("select rate from product where pid=%s;", id)
    data2 = cur.fetchone()
    return render_template("product_rate.html",data=data,data1=data1,data2=data2)
######################################################## add product ############################################
@app.route('/addproduct/',methods = ['GET', 'POST'])
def addproduct():
    if request.method == 'POST':
        user_details = request.form
        pid=str(user_details['pid'])
        pname=str(user_details['pname'])
        rate=str(user_details['rate'])
        cur.execute("insert into product (pid,pname,rate) values (%s,%s,%s);",(pid,pname,rate))
        conn.commit()
        cur.execute("select * from product")
        data=cur.fetchall()
        return render_template("product_update.html",data=data)
    return render_template('addproduct.html')
###################################################### Quantity Edit ##########################################
@app.route('/qtyedit/<pid>/<uid>',methods = ['GET', 'POST'])
def qtyedit(pid,uid):
    if request.method == 'POST':
        user_details = request.form
        update_qty=str(user_details['qty'])
        cur.execute("update order1 set qty=%s where uid=%s and pid=%s; ",(update_qty,uid,pid))
        conn.commit()
        cur.execute(
            "select u.uid,u.uname,p.pid,p.pname,o.qty from user u,product p,order1 o where u.uid=o.uid and p.pid=o.pid;")
        data = cur.fetchall()
        return render_template('view.html', data=data)
    return render_template("qtyupdate.html")
######################################################## User quantity udate #######################################


#######################################################  ADMINVIEW  ###################################################
@app.route('/view/',methods = ['GET', 'POST'])
def view():
    cur.execute("select u.uid,u.uname,p.pid,p.pname,o.qty from user u,product p,order1 o where u.uid=o.uid and p.pid=o.pid;")
    data=cur.fetchall()
    return render_template('view.html',data=data)
##################################################### Product Upadte ###################################
@app.route('/product_update/', methods = ['GET', 'POST'])
def product_update():
    cur.execute("select * from product")
    data=cur.fetchall()
    return render_template("product_update.html",data=data)
#################################################### Products #############################################
@app.route('/products/<id>', methods = ['GET', 'POST'])
def products(id):
    return redirect(url_for("addtocart",id1=id))
#################################################### Admin ##############################################
@app.route('/admin/', methods = ['GET', 'POST'])
def admin():
    return render_template('admin.html')
#################################################### STUDENT #############################################
@app.route('/studentlogin/', methods = ['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        user_details = request.form
        uname = str(user_details['name'])
        id = str(user_details['id'])
        phno=str(user_details['phno'])
        cur.execute("insert into user (uid,uname,phno) values (%s,%s,%s);", (id, uname, phno))
        conn.commit()

    return render_template('studentlogin.html')
############################################# Admin Login ################################################
@app.route('/adminlogin/', methods = ['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        user_details = request.form
        password = str(user_details['pass'])
        id = str(user_details['id'])
        try:
            cur.execute("select aid from admin where aid =%s;", id)
            mroll = cur.fetchone()
            mroll = str(mroll[0])
            cur.execute("select ananme from admin where aid =%s;", id)
            pas = cur.fetchone()
            pas = str(pas[0])
            if id == mroll:
                if pas == password:
                    return render_template('admin.html')
                else:
                    return "password incorrect"
        except:
            return "invalid id"
    return render_template("adminlogin.html")

########################################### MAIN_FUNCTION #################################################
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug='true')