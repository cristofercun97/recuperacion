from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Length, Email 

class LoginForm(FlaskForm):
    email=StringField('Correo eléctronico', validators=[DataRequired(), Email()])
    password=PasswordField('Contraseña', validators=[DataRequired(), Email()])
    submit=SubmitField('Acceder') 
    
class RegisterForm(FlaskForm):
    fullname=StringField('Nombre & Apellidps', validators=[DataRequired(), Length(min=3, max=50)])
    email=StringField('Correo eléctronico', validators=[DataRequired(), Email()])
    password=PasswordField('Contraseña', validators=[DataRequired(), Email()])
    submit=SubmitField('Acceder') 
    
class SubirFoto(FlaskForm):
    foto=StringField('foto', validators=[DataRequired(), Length(max=255)])
    descripcion=StringField('Descripcion', validators=[DataRequired(), Length(min=3, max=50)])
    submit=SubmitField('Enviar')