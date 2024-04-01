from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class TrabajadorForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    compleacomulada = StringField('Complejidad', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
class SupportForm(FlaskForm):
    description = StringField('Descripcion', validators=[DataRequired()])
    complejidad = StringField('Complejidad', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
