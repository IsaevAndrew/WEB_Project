from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, IntegerField, SelectField
from wtforms import FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed,FileField



class BooksForm(FlaskForm):
    content1 = SelectField("Автор")
    content2 = StringField("Название")
    content3 = IntegerField("Год")
    content4 = StringField("Издательство")
    content5 = SelectField("Жанр")
    content6 = FileField(
        "Фотография",
        validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                "Файл должен быть одного из этих форматов: 'jpg', 'png', 'jpeg'")])
    submit = SubmitField('Применить')