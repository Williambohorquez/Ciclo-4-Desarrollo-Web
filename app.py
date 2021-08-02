from flask import Flask, render_template, request, send_from_directory, flash
from markupsafe import escape
import yagmail
from utils import isUsernameValid, isPasswordValid


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method=='POST':
        user= escape(request.form['user'])
        password = escape(request.form['pass'])
        if user.lower()=="prueba" and password=="Prueba1234" and isUsernameValid(user) and isPasswordValid(password):
            return render_template('gallery.html')
        else:
            flash("Los datos proporcionados son inválidos")
            return render_template('index.html')
    else:
        return render_template('index.html')

    
@app.route('/forgot/', methods=["GET", "POST"])
def forgot():
    if (request.method=="POST"):
        email=escape(request.form['email'])
        if (email==''):
            flash("Debe escribir una dirección de correo electrónico válida.")
        else:        
            yag = yagmail.SMTP('soporte.pictic@gmail.com','UniNorte2022')
            yag.send(to=email, subject="Recuperación de la contraseña", contents="Para cambiar su contraseña presione por favor en <a href='https://www.google.com.co'>este enlace</a>")
            flash("Si escribió una dirección de correo válida, puede revisar su bandeja de entrada o a veces es necesario revisar la bandeja de SPAM. ")
    return render_template("forgot.html") 

@app.route('/gallery/', methods=["GET", "POST"])
def gallery():
    return render_template("gallery.html")

@app.route('/download/<string:id>', methods=["GET", "POST"])
def download(id):
    name='imagen'+escape(id)+'.png'
    try:
        return send_from_directory('static/img/users/user1', filename=name, as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/login/')
def loginD():
    return login()

@app.route('/register/')
def register():
    return render_template("register.html")


