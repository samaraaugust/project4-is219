from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from app.recipes.forms import new_recipe
from app.db.models import Recipes
from jinja2 import TemplateNotFound
from app.db import db
from werkzeug.utils import secure_filename
recipes = Blueprint('recipes', __name__,
                        template_folder='templates')

@recipes.route('/create', methods=['POST', 'GET'])
@login_required
def upload():
    form = new_recipe()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        print("name: ", filename)
        """
        recipe = Recipes(title=form.title.data, description=form.description.data,
                         image=form.image.data, ingredients=form.ingredients.data)
        current_user.recipes = recipe
        db.session.commit()
        """
    try:
        return render_template('create_recipe.html', form=form)
    except TemplateNotFound:
        abort(404)