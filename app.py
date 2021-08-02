import os
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, send_file, session, g
from markupsafe import escape
import yagmail
from utils import isUsernameValid, isPasswordValid, isEmailValid, isValidPic
from db import conectar, desconectar
import hashlib
import random
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
app.secret_key = os.urandom(24) #Para ataques CSRF
yag = yagmail.SMTP('soporte.pictic@gmail.com','UniNorte2022')

@app.route('/', methods=["GET", "POST"])
def login():
    try:
        if g.user and request.method=='GET':
            if g.user[5]!='A':
                flash("Su usuario no se encuentra apto para iniciar sesión")
                return render_template('index.html')
            else:
                return redirect('/profile')
        if request.method=='POST':

            user= escape(request.form['user'])
            password = escape(request.form['pass'])
            
            if not isPasswordValid(password) or not isEmailValid(user):

                if not isPasswordValid(password) :
                    flash ('Su contraseña debe tener mínimo 8 caracteres y contener mínimo 1 mayúscula, 1 minúscula y un número')

                if not isEmailValid(user):
                    flash ('Debe escribir un correo válido')

                return render_template( 'index.html' )


            sql = 'SELECT password, status, nickname, profile, last_access, id FROM users WHERE email = ?'
            res = conectar().execute(sql, (user,)).fetchone()
            
            if res is None:
                error = 'Usuario o contraseña inválidos' # Para no decirle al usuario directamente que el usuario no existe y evitar darle información a un atacante
                flash( error )
                return render_template( 'index.html' )

            if (check_password_hash(res[0], password)):
               

                if (res[1]=='A'):
                    session.clear()
                    session['userID']=user
                    session['ID']=res[5]
                    session['nickname']=res[2]
                    session['profile']=res[3]
                    session['last_access']=res[4]

                    now= time.strftime("%x") + " " + time.strftime("%X")
                    sql = 'update users set last_access=? where email=?'
                    datab=conectar()
                    datab.execute(sql, (now, user))
                    datab.commit()
                    desconectar()

                    return redirect('/profile')

                elif (res[1]=='C'):
                    flash("El usuario no ha realizado el proceso de activación mediante correo")
                elif (res[1]=='I'):
                    flash("El usuario está inhabilitado en la plataforma")
                elif (res[1]=='B'):
                    flash("El usuario está bloqueado por múltiples intentos de acceso, puede reestablecer su contraseña desde el siguiente enlace:")
                    return render_template('index.html', link='forgot')
            else:
                flash("El usuario no existe en la base de datos o los datos son incorrectos")  # Para no decirle al usuario directamente que la contraseña fue errónea y así evitar darle información a un atacante
        
        return render_template('index.html')
    except:
        return render_template( 'index.html' )

@app.route('/login/', methods=["GET", "POST"])
@app.route('/index/', methods=["GET", "POST"])
def index():
    try:
        if g.user and request.method=='GET':
            if g.user[5]!='A':
                flash("Su usuario no se encuentra apto para iniciar sesión")
                return render_template('index.html')
        return redirect ('/')
    except:
        pass


@app.route('/forgot/', methods=["GET", "POST"])
def forgot():
    if 'userID' in session:
        return redirect('/')
    if (request.method=="POST"):
        email=escape(request.form['email'])
        if (email=='' or not isEmailValid(email)):
            flash("Debe escribir una dirección de correo electrónico válida.")
            return render_template("forgot.html") 
            
        else:
            
            sql = 'SELECT nickname, status FROM users WHERE email = ?'
            res = conectar().execute(sql, (email,)).fetchone()
            
            if res != None:
                if (res[1]=='A'):
                    user= res[0]
                    text  = GenMD5(email)
                    enc = hashlib.md5(text.encode())
                    
                    sql = 'update users set link=? where email=?'
                    datab=conectar()
                    datab.execute(sql, (enc.hexdigest(), email))
                    datab.commit()
                    desconectar()


                    yag.send(to=email, subject="Recuperación de la contraseña", contents="Para cambiar su contraseña siga por favor este enlace: http://localhost:5000/reset/" + user + '/' + enc.hexdigest())
                    flash("Puede revisar su bandeja de entrada o a veces es necesario revisar la bandeja de SPAM. ")
                    return render_template("forgot.html") 
                else:
                    flash("La cuenta de correo no se encuentra activa")
                    return render_template("forgot.html")  
            flash("No se encontró ese correo en nuestra base de datos")
    return render_template("forgot.html")  


@app.route('/download/<string:user>/<string:img>', methods=["GET", "POST"])
def download(user,img):
    user=escape(user)
    img=escape(img)
    if 'nickname' in session:
        enc= session['nickname']
        enc = hashlib.md5(enc.encode())
        
        if enc.hexdigest() != user:

            sql='select id from pictures where public=? and pic_hash=? '
            res = conectar().execute(sql, (True,img)).fetchone()
            if res != None:
                path= 'static/img/users/'+user+'/'+img
            else:
                flash ("Se produjo un error al intentar descargar la imagen solicitada, es posible que la imagen ya no exista en el servidor")
                return redirect('/profile')
        else:    
            path= 'static/img/users/'+user+'/'+img
    else:
        sql='select id from pictures where public=? and pic_hash=? '
        res = conectar().execute(sql, (True,img)).fetchone()
        if res != None:
            path= 'static/img/users/'+user+'/'+img
        else:
            flash ("Se produjo un error al intentar descargar la imagen solicitada")
            return redirect('/')
    try:
        return send_file(path, attachment_filename="imagen.jpg", as_attachment=True)
    except Exception as e:
        flash ("Se produjo un error al intentar descargar la imagen solicitada, es posible que la imagen ya no exista en el servidor")
        retur


@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method=='POST':
        user= escape(request.form['user'])
        password = escape(request.form['pass1'])
        email = escape(request.form['email'])
        if isUsernameValid(user) and isPasswordValid(password) and isEmailValid(email):

            datab=conectar()
            if datab != None:
                
                enc = hashlib.md5(GenMD5(email).encode())
                password = generate_password_hash(password)

                desconectar()
                sql = 'SELECT id FROM users WHERE nickname = ?'
                res = conectar().execute(sql, (user,)).fetchone()
                desconectar()

                if res != None:
                    flash("El nombre de usuario ya existe en la base de datos, por favor utilice otro nombre de usuario")
                    return render_template("register.html", email=email)

                sql = 'SELECT id FROM users WHERE email = ?'
                res = conectar().execute(sql, (email,)).fetchone()
                if res != None:
                    flash("Ya existe un usuario con ese correo, por favor inicie sesión con ese correo o utilice la opción de recuperar contraseña si la olvidó.")
                    return redirect('/')


                sql = 'INSERT INTO users(nickname,password,email,status,link) VALUES(?,?,?,?,?)'
                datab=conectar()
                datab.execute(sql, (str(user), password, str(email), 'C', enc.hexdigest()))
                datab.commit()
                desconectar()

                yag.send(to=email, subject="Activación de su cuenta", contents="Para activar su cuenta en PicTIC por favor ingrese con este enlace: http://localhost:5000/activate/" + user + '/' + enc.hexdigest())
                flash("Si escribió una dirección de correo válida, debe activar su cuenta mediante el enlace que le fue enviado, puede revisar su bandeja de entrada o a veces es necesario revisar la bandeja de SPAM. ")
            else:
                flash("Sin conexión con la base de datos")
                
                
        else:
            if not isUsernameValid(user):
                flash("El usuario no puede contener caracteres especiales ni espacio")
                return render_template("register.html", email=email, nickname=user)

            if not isPasswordValid(password):
                flash("Su contraseña debe tener mínimo 8 caracteres y contener mínimo 1 mayúscula, 1 minúscula y un número")
                return render_template("register.html", email=email, nickname=user)

            if not isEmailValid(email):
                flash("No escribió un correo válido")
                return render_template("register.html", nickname=user)
            return render_template("register.html")
        return redirect('/')
    else:
        if 'userID' in session:
            return redirect('/')
        else:
            return render_template("register.html")

@app.route('/profile/', methods=["GET", "POST"])
def profile():
    if 'userID' in session:
        if (request.method=="GET"):
            
            sql = 'SELECT nickname, password, status, link, profilepic, profile, id FROM users WHERE email = ?'
            res = conectar().execute(sql, (session['userID'],)).fetchone()

            nickCyp = hashlib.md5(res[0].encode())
            nickCyp = nickCyp.hexdigest()

            sql = 'SELECT pic_hash, description, tags, public FROM pictures WHERE reported=? and user_id = ?'
            contenido = conectar().execute(sql, (False, res[6])).fetchall()

            paths=[]
            for item in contenido:
                paths.append(["../static/img/users/"+nickCyp,item[0], item[1], item[2], item[3]])
            if res[4]!= None:
                profileP="static/img/users/"+nickCyp+"/"+res[4]
            else:
                profileP=''
            return render_template('profile.html', nickname=res[0], email=session['userID'], profileP=profileP, pictures=paths, nickCyp=nickCyp)
    return redirect('/')

@app.route('/submitImg', methods=["POST","GET"])
def submitImg():
    if (request.method=="POST"):
        try:
            form_name = request.form['form-name']
            if form_name == 'Eliminar':
                id= escape(str(session['ID']))
                
                name= escape(request.form['nameImg'])

                enc= str(session['nickname'])
                enc = hashlib.md5(enc.encode()).hexdigest()

                sql ='delete from pictures where id=(select pictures.id from pictures join users on users.id=pictures.user_id  where pictures.user_id=? and pictures.pic_hash=?)'
                datab=conectar()
                datab.execute(sql, (id, name))
                datab.commit()
                desconectar()

                archivo=os.path.join(app.root_path, 'static', 'img', 'users',enc,name)
                os.remove(archivo)
                flash(archivo)
                flash("Se eliminó correctamente la imagen.")

            elif form_name == 'Guardar':
                
                sql = 'SELECT id FROM users WHERE nickname = ?'
                res = conectar().execute(sql, (escape(session['nickname']),)).fetchone()
                desconectar()


                if res != None:
                    id = res[0]
                    name= escape(request.form['nameImg'])
                    sql = 'SELECT id FROM pictures WHERE user_id = ? and pic_hash = ?'
                    res = conectar().execute(sql, (id, name)).fetchone()
                    desconectar()
                    if res != None:

                        tags= escape(request.form['tagsImg'])
                        description= escape(request.form['descriptionImg'])
                        
                        if 'publicImg' in request.form:
                            public=True
                        else:
                            public=False
                
                        sql = 'update pictures set tags = ?, description = ?, public = ? where user_id = ? and pic_hash = ?'
                        datab=conectar()
                        datab.execute(sql, (tags, description, public, id, name))
                        datab.commit()
                        desconectar()

                        flash("Se actualizaron los datos de la imagen correctamente.")
                    else:
                        flash("No puede ejecutar esta acción, porque la foto no pertenece al usuario que inició sesión.")

                else:
                    flash("No hay sesión de usuario iniciada para ejecutar esta acción.")
            return redirect('/profile')
        except:
            
            flash("Se presentó un error al efectuar la acción.")
    return redirect('/profile')
                
            

@app.route('/upload', methods=["POST","GET"])
def upload():
    
    if (request.method=="POST"):
        try:
            form_name = request.form['form-name']
            if form_name == 'subir':
                f =  request.files['upload']
                enc= str(session['nickname'])
                enc = hashlib.md5(enc.encode()).hexdigest()
                fn=''+secure_filename(f.filename)
                if fn.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):

                    tags= escape(request.form['tags'])
                    description= escape(request.form['description'])


                    if 'public' in request.form:
                        public=True
                    else:
                        public=False
                
                    fn=GenMD5(fn)
                    archivo=os.path.join(app.root_path, 'static', 'img', 'users',enc,fn)
                    f.save(archivo)
                    
                    if isValidPic(archivo):
                        datab=conectar()
                        datab.execute(
                                'INSERT INTO pictures (pic_hash, user_id, tags, description, public) VALUES (?,?,?,?,?)',
                                (fn, g.user[0], tags, description, public)
                            )
                        datab.commit()
                        desconectar()
                        flash("Imagen subida con éxito")
                    else:
                        os.remove(archivo)
                        flash("EL archivo no superó la verificación de ser una imagen y no pudo ser alojado en el servidor")
                else:
                    flash("El archivo " + fn + " tiene una extensión no válida ")

        except:
                flash("Se presentó un error al subir la imagen")
    return redirect('/profile')


@app.route('/edit/')
def edition():
    return render_template("edition.html")


@app.route('/activate/<string:user>/<string:link>')
def activate(user, link):
    
    datab=conectar()
    if datab != None:
        
        sql = 'SELECT nickname FROM users WHERE nickname = ? and link = ?'
        res = conectar().execute(sql, (str(user),link)).fetchone()
        desconectar()

        if res != None:

            sql = 'update users set status=? where nickname=? and link=?'
            datab=conectar()
            datab.execute(sql, ('A', str(user), link))
            datab.commit()
            desconectar()

            folder= '' + str(user)
            folder = hashlib.md5(folder.encode())
            folder='static/img/users/'+folder.hexdigest()
            if not os.path.exists(folder):
                os.makedirs(folder)
            flash("Su usuario ha sido activado con éxito")
        else:
            flash("No se encontró ningún usuario para ser activado con ese enlace")
            
    else:
        flash("No hay conexión con la base de datos")
    return redirect('/')

    
@app.route('/reset/<string:user>/<string:link>', methods=["GET", "POST"])
def reset(user, link):
    if request.method=='POST':
        password = escape(request.form['pass1'])
        password2 = escape(request.form['pass2'])
        if password != password2:
            flash("Debe escribir la misma contraseña en los 2 campos")
        else:
            if not isPasswordValid(password):
                flash("Su contraseña debe tener mínimo 8 caracteres y contener mínimo 1 mayúscula, 1 minúscula y un número")
            else:
                datab=conectar()
                if datab != None:
                    
                    sql = 'SELECT nickname, status FROM users WHERE nickname = ?  and link = ?'
                    res = conectar().execute(sql, (escape(str(user)), escape(link))).fetchone()
                    desconectar()
                    
                    if res != None:
                        
                        password = generate_password_hash(password)
                        link=GenMD5(user)

                        sql = 'update users set password = ? where nickname= ?'
                        datab=conectar()
                        datab.execute(sql, (password, str(user)))
                        datab.commit()
                        desconectar()

                        flash("Su contraseña ha sido actualizada exitosamente ha sido activado con éxito")
                    else:
                        flash("No se encontró ningún usuario para cambio de contraseña con ese enlace")
                        
                else:
                    flash("No hay conexión con la base de datos")
                return redirect('/')
    return render_template("resetPass.html")



@app.route('/logout/')
def logout():
    if 'userID' in session:
        g.user = None
        session.clear()
        desconectar()
        g.pop('user',None)
        flash ("Salió del sistema")
    return redirect('/')


def GenMD5(param):
    enc= '' + str(random.randrange(100000)) + str(param) + str(random.randrange(100000))
    enc = hashlib.md5(enc.encode())
    return enc.hexdigest()


@app.before_request
def load_logged_in_user():
    if 'userID' in session:
        g.user = conectar().execute('SELECT * FROM users WHERE email = ?', (session['userID'],)).fetchone()
    else:
        g.user = None
        
@app.route('/gallery/',methods=["GET","POST"])
def gallery():
    tags=''
    if (request.method=="GET"):
        sql = 'select pictures.pic_hash, pictures.tags, users.nickname from pictures join users on users.id=pictures.user_id where pictures.public=?'
        contenido = conectar().execute(sql, (True,)).fetchall()

    else:
        tags = '%' + escape(request.form['Buscar']).lower() + '%'
        sql = "select pictures.pic_hash, pictures.tags, users.nickname from pictures join users on users.id=pictures.user_id where pictures.public=? and pictures.tags like ?"
        contenido = conectar().execute(sql, (True,tags)).fetchall()

    
    
    paths=[]
    contador=0
    for item in contenido:
        enc= str(item[2])
        enc = hashlib.md5(enc.encode())
        paths.append(["../../static/img/users/"+enc.hexdigest(),item[0],item[1],enc.hexdigest()])
        contador+=1
    if contador==0 and (request.method=="POST"):
        flash("No se encontraron imágenes con ese tag.")
    elif contador==0:
        flash("Aún no hay imágenes públicas para visualizar.")
    else:
        if tags!='':
            if contador ==1:
                flash("Se encontró 1 imagen pública que contiene ese tag.")
            else:
                flash("Se encontraron " + str(contador) + " imágenes públicas que contienen ese tag.")
    return render_template('gallery.html', pictures=paths)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=('certificate.crt','private.key'))
    