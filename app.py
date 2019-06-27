from flask import Flask , render_template,\
    flash, redirect , url_for , session ,request, logging
     
from flask_mysqldb import MySQL 

from data import Articles
from wtforms import Form, StringField , TextAreaField ,PasswordField , validators 
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.debug = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

Articles = Articles()


@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html' , articles = Articles )

@app.route('/articles/<int:id>/') 
def article(id):
    return render_template('article.html',id=id , articles = Articles) 

class RegisterForm(Form): 
    name = StringField('Name',[validators.Length(min=1,max=50)]) 
    username = StringField('Username',[validators.Length(min=4,max=25)]) 
    email = StringField('Email',[validators.Length(min=4,max=25)]) 
    password = PasswordField('Password', [ validators.DataRequired(),validators.EqualTo('confirm',message ='passwords do not match')]) 
    confirm = PasswordField('Confirm password') 

@app.route('/register', methods=['GET','POST']) 
def register():
    form = RegisterForm(request.form) 
    if request.method == 'POST' and form.validate():
        name = form.name.data  
        email = form.email.data  
        username = form.username.data  
        password = sha256_crypt.encrypt(str(form.password.data)) 

        #create cusor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))

        #commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        flash("You are now Registerd and you can login", 'success') 

        redirect(url_for('login'))
        redirect(url_for('index')) 


    return render_template('register.html',form=form) 

if __name__ =='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()