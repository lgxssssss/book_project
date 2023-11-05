from flask import Flask
from flask import request,session
from flask import render_template 
from flask import redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import logging
import json
import os
import sqlite3 
import time


from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory


app = Flask(__name__)
app.secret_key = '(&$@X?>"|AA|S:"^%$")|='
DATABASE = 'test.db'
UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.context_processor
def inject_user():
    user = None
    if"username" in session:
        user = session["username"]
    return dict(user = user)


# 主界面

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from books where 1=1'
    cursor.execute(sql)
    res = cursor.fetchall()
    return render_template("index.html",books = res)

# 登陆界面

@app.route('/login', methods=['GET'])
def login_get():
    if"username" in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

# @app.route('/login', methods=['POST'])
# def login_post():
#     input_username = request.form['username']
#     input_pwd = request.form['password'] 
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     sql = 'select * from users where username=?'
#     cursor.execute(sql, (input_username,))
#     res = cursor.fetchall()
#     if (len(res)) == 0:
#         return redirect(url_for("signin_form"))
#     else:
#         _, _, real_password = res[0]
#         if real_password == input_pwd:
#             session['username'] = input_username
#             return redirect(url_for("home"))
#         else:
#             return render_template('result.html',t=2)
        
@app.route('/query_user', methods=['POST']) 
def query_user():
    input_username = request.form['username']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from users where username=?'
    cursor.execute(sql, (input_username,))
    res = cursor.fetchall()
    if (len(res)) == 0:
        return {"code": -9999, "message": "username is not existed!"}
    else:
        return {"code": 0, "message": "username is existed!"}
    

@app.route('/query_login', methods=['POST']) 
def query_login():
    input_username = request.form['username']
    input_pwd = request.form['password'] 
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from users where username=?'
    cursor.execute(sql, (input_username,))
    res = cursor.fetchall()
    if (len(res)) == 0:
        # return redirect(url_for("signin_form"))
        return {"code": -1, "message": "username is not existed!"}
    else:
        _, _, real_password = res[0]
        if real_password == input_pwd:
            session['username'] = input_username
            return {"code": 0, "message": "login sucess"}
        else:
            return {"code": -2, "message": "password is worring!!"}

# 退出

@app.route('/logout') 
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))

# 注册界面

@app.route('/register', methods=['GET'])
def register_get():
    return render_template("register.html")

# @app.route('/register', methods=['POST'])  
# def register_post():
#     input_username = request.form['username']   
#     input_pwd = request.form['password']  
#     conn = sqlite3.connect(DATABASE)  
#     cursor = conn.cursor() 
#     sql = "select * from users where username=?" 
#     cursor.execute(sql,(input_username,)) 
#     res = cursor.fetchall() 
#     if(len(res)) == 0:  
#         sql ="insert into users (username,password) values ('{}','{}')".format(input_username,input_pwd)
#         cursor.execute(sql)
#         conn.commit()
#         return render_template('result.html',t=0,username = input_username) 
#     else:
#         return render_template('result.html',t=1)
    
@app.route('/query_register', methods=['POST'])  
def query_register_a():
    input_username = request.form['username']   
    input_pwd = request.form['password']  
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor() 
    sql = "select * from users where username=?" 
    cursor.execute(sql,(input_username,)) 
    res = cursor.fetchall() 
    if(len(res)) == 0:  
        sql ="insert into users (username,password) values ('{}','{}')".format(input_username,input_pwd)
        cursor.execute(sql)
        conn.commit()
        return {"code": 0, "message": "login sucess"} 
    else:
        return {"code": -1, "message": "user is existed!!"}
    
# 图书创建

@app.route('/book/create', methods=['GET'])
def book_create_get():
    return render_template("book_create.html")


# @app.route('/book/create', methods=['POST'])
# def book_form():
#     input_book_name = request.form['book_name']   
#     input_price = request.form['price']  
#     input_book_desc = request.form['book_desc']  
#     conn = sqlite3.connect(DATABASE)  
#     cursor = conn.cursor() 
#     sql = "select * from books where book_name=?" 
#     cursor.execute(sql,(input_book_name,)) 
#     if(len(input_book_name) > 0):
#         try:
#             input_price = float(input_price)
#         except:
#             return "price 填错了"
#         if 'file' in request.files:
#             file = request.files['file']
#             if file.filename != '':
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     file.save(os.path.join(UPLOAD_FOLDER, filename))
#                     sql ="insert into books (book_name,title_image,price,book_desc) values ('{}','{}',{},'{}')".format(input_book_name,filename,input_price,input_book_desc)
#                     cursor.execute(sql)
#                     conn.commit()
#                     return "图书创建成功"
#                 else:
#                     return "文件类型不符合要求"
#             else:
#                 return "图片有问题"
#         else:
#             return "图片不存在"
#     else:
#         return "名字输入错误"


# @app.route('/book_create_quary', methods=['POST'])
# def book_create_quary():
#     input_book_name = request.form['book_name']   
#     input_price = request.form['price']  
#     input_book_desc = request.form['book_desc']
#     conn = sqlite3.connect(DATABASE)  
#     cursor = conn.cursor() 
#     sql = "select * from books where book_name=?" 
#     cursor.execute(sql,(input_book_name,)) 
#     if(len(input_book_name) > 0):
#         try:
#             input_price = float(input_price)
#         except:
#             return "price 填错了"
#         if 'file' not in request.files:
#             return {"code": -2, "message": "not picture"}
#         file = request.files['file'] 
#         if file.filename == '':
#             return {"code": -3, "message": "picturename is null "}
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             sql ="insert into books (book_name,title_image,price,book_desc) values ('{}','{}',{},'{}')".format(input_book_name,filename,input_price,input_book_desc)
#             cursor.execute(sql)
#             conn.commit()
#             return {"code": 0, "message": "create sucess"}
#     return {"code": -1, "message": "创建失败"}

@app.route('/book_create_quary', methods=[ 'POST'])
def book_create_quary():

        input_book_name = request.form['book_name']   
        input_price = request.form['price']  
        input_book_desc = request.form['book_desc']
        conn = sqlite3.connect(DATABASE)  
        cursor = conn.cursor() 
        sql = "select * from books where book_name=?" 
        cursor.execute(sql,(input_book_name,))
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            sql ="insert into books (book_name,title_image,price,book_desc) values ('{}','{}',{},'{}')".format(input_book_name,filename,input_price,input_book_desc)
            cursor.execute(sql)
            conn.commit()
            return '{"filename":"%s"}' % filename



    #     if 'file' in request.files:
    #         file = request.files['file']
    #         if file.filename != '':
    #             if file and allowed_file(file.filename):
    #                 filename = secure_filename(file.filename)
    #                 file.save(os.path.join(UPLOAD_FOLDER, filename))
    #                 sql ="insert into books (book_name,title_image,price,book_desc) values ('{}','{}',{},'{}')".format(input_book_name,filename,input_price,input_book_desc)
    #                 cursor.execute(sql)
    #                 conn.commit()
    #                 return "图书创建成功"
    #             else:
    #                 return "文件类型不符合要求"
    #         else:
    #             return "图片有问题"
    #     else:
    #         return "图片不存在"
    # else:
    #     return "名字输入错误"
    
    
    
# 图书售卖

@app.route('/book/<book_id>', methods=['GET'])
def get_book_info(book_id):
    # user = None
    # if "username" in session:
    #     user = session["username"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from books where id = ?'
    cursor.execute(sql, (book_id,))
    res = cursor.fetchall()[0]
    return render_template("book_info.html", book = res)

# 订单

@app.route('/order', methods=['GET'])
def get_order():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from orders where 1=1 '
    cursor.execute(sql)
    res = cursor.fetchall()
    return render_template("order.html", order = res)

# @app.route('/order', methods=['POST']) 
# def order_post():
#     user = None
#     if "username" in session:
#         user = session["username"]
#     conn = sqlite3.connect(DATABASE)  
#     cursor = conn.cursor() 
#     input_book_id = request.form['book_id']
#     sql = "select * from books where id=?" 
#     cursor.execute(sql,(input_book_id,)) 
#     res1 = cursor.fetchall()
#     sql = "select * from users where username=?" 
#     cursor.execute(sql,(user,)) 
#     res2 = cursor.fetchall()
#     # return str(res2)
#     if len(res1) !=0:
#         if len(res2) !=0:
#             real_bookname = res1[0][1]
#             real_userid = res2[0][0]
#             real_price = res1[0][2]
#             num = 1
#             sql = "insert into orders (username,bookname,userid,bookid,allprice,num) values ('{}','{}',{},{},{},'{}')".format(user,real_bookname,real_userid,input_book_id,real_price,num)
#             cursor.execute(sql)
#             conn.commit()
#             return "购买成功"
#         else:
#             return "用户不存在"
#     else:
#         return "书籍不存在"


@app.route('/query_buy', methods=['POST']) 
def query_buy():
    user = None
    if "username" in session:
        user = session["username"]
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor() 
    input_book_id = request.form['book_id']
    sql = "select * from books where id=?" 
    cursor.execute(sql,(input_book_id,)) 
    res1 = cursor.fetchall()
    sql = "select * from users where username=?" 
    cursor.execute(sql,(user,)) 
    res2 = cursor.fetchall()
    # return str(res2)
    if len(res1) !=0:
        if len(res2) !=0:
            real_bookname = res1[0][1]
            real_userid = res2[0][0]
            real_price = res1[0][2]
            num = 1
            sql = "insert into orders (username,bookname,userid,bookid,allprice,num) values ('{}','{}',{},{},{},'{}')".format(user,real_bookname,real_userid,input_book_id,real_price,num)
            cursor.execute(sql)
            conn.commit()
            return {"code": 0, "message": "buy sucess"}
        else:
            return {"code": -1, "message": "user is not exist"}
    else:
        return {"code": -2, "message": "book is not exist"}
    

    
@app.route('/query_order_delect', methods=['POST']) 
def query_order_delect():
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor() 
    input_oid_id = request.form['oid']
    sql = "select * from orders where oid=?" 
    cursor.execute(sql,(input_oid_id,)) 
    res = cursor.fetchall()
    if len(res) !=0:
        sql = "DELETE FROM orders WHERE oid={} ".format(input_oid_id)
        cursor.execute(sql)
        conn.commit()
        return {"code": 0, "message": "order delect sucess"}
    else:
        return {"code": -1, "message": "order delect failed"}


if __name__ == '__main__':
    app.run()
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.run(debug=True, host='0.0.0.0')