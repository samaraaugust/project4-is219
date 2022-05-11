from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class new_recipe(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300), validators.DataRequired()])
    description = TextAreaField('Description', [validators.length(min=1, max=300), validators.DataRequired()])
    ingredients = TextAreaField('Ingredients', [validators.length(min=1, max=300), validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
    submit = SubmitField()

class edit_recipe(FlaskForm):
    title = TextAreaField('Title', [validators.length(min=1, max=300), validators.DataRequired()])
    description = TextAreaField('Description', [validators.length(min=1, max=300), validators.DataRequired()])
    ingredients = TextAreaField('Ingredients', [validators.length(min=1, max=300), validators.DataRequired()])
    image = FileField('Image', [validators.DataRequired()])
    submit = SubmitField()

class search_food(FlaskForm):
    search = TextAreaField('Search', [validators.length(min=1, max=300), validators.DataRequired()])
    submit = SubmitField()