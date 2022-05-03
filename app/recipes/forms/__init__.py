from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class new_recipe(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300)])
    description = TextAreaField('Description', [validators.length(min=1, max=300)])
    ingredients = TextAreaField('Ingredients', [validators.length(min=1, max=300)])
    image = FileField('Image')
    submit = SubmitField()