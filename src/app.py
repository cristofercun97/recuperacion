from flask import Flask, render_template, redirect,request,url_for,flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf import CSRFProtect
from config import Config 
from models.entities.User import User
from models.ModelUser import ModelUser 
from form import LoginForm, RegisterForm, SubirFoto


#instacias
app=Flask(__name__)
mysql= MySQL(app)
csrf= CSRFProtect(app)
login_manager= LoginManager(app)
app.config.from_object(Config)

#Verificación de formulario
@app.before_request
def check_environment():
    if app.config['ENV'] == 'development':
        print('Modo de desarollo activado.')

#Carga de los usuarios
@login_manager.user_loader
def loader_user(id):
    return ModelUser.get_by_id(mysql, id) 

#Ruta login
@app.route('/login', methods=['GET','POST'])

def login():
    form =LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))
    if request.method=='POST':
        email= request.form['email']
        password= request.form['password']
        user=User(0,None,email,password)
        
        logged_user=ModelUser.login(mysql, user)
        if logged_user:
            login_user(logged_user)
            flash('Sesión iniciada con éxito.')
            return redirect(url_for('perfil'))
        else:
            flash('Usuario o Contraseña incorrectas vuleve a intentarlo.')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form= RegisterForm()
    if request.method=='POST':
        fullname=request.form['fullname']
        email=request.form['email']
        password=request.form['password']
        
        user=User(0,fullname,email,password)
        
        register_user=ModelUser.register(mysql,user)
        if register_user:
            flash('Usuario registrado con éxito.')
            return redirect(url_for('login'))
        else:
            flash('Al parecer hubo un error al registrar al usuario.')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/perfil')

def perfil():
    form=SubirFoto()
    return render_template('perfil.html', form=form)

#protected
@app.route('/protected')
def protected():
    return '<h1> Lo sentimos esta ruta solamente pueden acceder usuarios autenticados.</h1>'

#Excepciones de Estados de error 

def status_401(error):
    return redirect(url_for('index.html'))

def status_404(error):
    return '<h1> Lo sentimos esta página no se pudo encontrar.</h1>'

#Vista de la ruta Raíz
@app.route('/')
def index():
    return render_template('index.html') 

#CRUD para que el usuario pueda subir y ver las fotos de los demas usuarios

if __name__ == '__main__':
    app.run(debug=True) 
    csrf.init_app(app)
    