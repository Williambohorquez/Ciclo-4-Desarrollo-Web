from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField  #Elementos que se van a utilizar del wtf
from wtforms.validators import DataRequired


class FrmLogin(FlaskForm):
    try:
        Tbuscar = StringField('Buscar Imagen')
        user = StringField('Usuario *',validators=[DataRequired(message='El campo es requerido')])
        password = PasswordField('Contraseña *',validators=[DataRequired(message='El campo es requerido')])
        recordar = BooleanField('Mantenerse conectado')
        btn = SubmitField('Iniciar sesión')
    except:
        pass

class FrmContactenos(FlaskForm):
    try:
        nombre = StringField('Nombre *',validators=[DataRequired(message='El campo es requerido')])
        usuario = StringField('Usuario *',validators=[DataRequired(message='El campo es requerido')])
        mensaje = StringField('Escriba su mensaje *',validators=[DataRequired(message='El campo es requerido')])
        enviar = SubmitField('Enviar')
    except:
        pass

class FrmGallery(FlaskForm):
    try:
        Titulo = "Galería de fotos" 
    except:
        pass

class FrmForgot(FlaskForm):
    try:
        Titulo = "Recuperación de contraseña" 
        email = StringField('Ingrese su correo para proceder con el envío del enlace de recuperación* ',validators=[DataRequired(message='El campo es requerido')])
        
    except:
        pass

    