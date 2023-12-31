from flask import Flask
from flask import request,session
from flask import render_template 
from flask import redirect,url_for
from werkzeug.utils import secure_filename
import sqlite3 
import os 

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
    # user = None
    # if "username" in session:
    #     user = session["username"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from books where 1=1'
    cursor.execute(sql)
    res = cursor.fetchall()
    return render_template("index.html",books = res)
    # return str(res)

# 登陆界面

@app.route('/login', methods=['GET'])
def login_get():
    if"username" in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    input_username = request.form['username']
    input_pwd = request.form['password'] 
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from users where username=?'
    cursor.execute(sql, (input_username,))
    res = cursor.fetchall()
    if (len(res)) == 0:
        return redirect(url_for("signin_form"))
    else:
        _, _, real_password = res[0]
        if real_password == input_pwd:
            session['username'] = input_username
            return redirect(url_for("home"))
        else:
            return render_template('result.html',t=2)

# 退出

@app.route('/logout') 
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))

# 注册界面

@app.route('/register', methods=['GET'])
def register_get():
    return render_template("register.html")

@app.route('/register', methods=['POST'])  
def register_post():
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
        return render_template('result.html',t=0,username = input_username) 
    else:
        return render_template('result.html',t=1)
    
# 图书创建

@app.route('/book/create', methods=['GET'])
def book_create_get():
    return render_template("book_create.html")


@app.route('/book/create', methods=['POST'])
def book_form():
    input_book_name = request.form['book_name']   
    input_price = request.form['price']  
    input_book_desc = request.form['book_desc']  
    conn = sqlite3.connect(DATABASE)  
    cursor = conn.cursor() 
    sql = "select * from books where book_name=?" 
    cursor.execute(sql,(input_book_name,)) 
    if(len(input_book_name) > 0):
        try:
            input_price = float(input_price)
        except:
            return "price 填错了"
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    sql ="insert into books (book_name,title_image,price,book_desc) values ('{}','{}',{},'{}')".format(input_book_name,filename,input_price,input_book_desc)
                    cursor.execute(sql)
                    conn.commit()
                    return "图书创建成功"
                else:
                    return "文件类型不符合要求"
            else:
                return "图片有问题"
        else:
            return "图片不存在"
    else:
        return "名字输入错误"
    
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
    # user = None
    # if "username" in session:
    #     user = session["username"]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = 'select * from orders where 1=1 '
    cursor.execute(sql)
    res = cursor.fetchall()
    return render_template("order.html", order = res)

@app.route('/order', methods=['POST']) 
def order_post():
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
            return "购买成功"
        else:
            return "用户不存在"
    else:
        return "书籍不存在"


if __name__ == '__main__':
    app.run()
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.run(debug=True, host='0.0.0.0')