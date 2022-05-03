from flask import Blueprint, render_template, abort, Request, Response
from flask_login import login_required, current_user
from app.recipes.forms import new_recipe
from app.db.models import Recipes, Image
from jinja2 import TemplateNotFound
from app.db import db
from werkzeug.utils import secure_filename
recipes = Blueprint('recipes', __name__,
                        template_folder='templates')

@recipes.route('/<int:id>', methods=['GET'])
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return "no image with is", 404
    return Response(img.img, mimetype=img.mimetype)

@recipes.route('/create', methods=['POST', 'GET'])
@login_required
def upload():
    form = new_recipe()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        print("name: ", filename)
        mimetype = form.image.data.mimetype
        print("mime: ", mimetype)
        image2 = Image(img=form.image.data.read(), name=filename, mimetype=mimetype)
        db.session.add(image2)
        db.session.commit()
        imageID = image2.id
        print("Image id: ", imageID)
        recipe = Recipes(title=form.title.data, description=form.description.data,
                         image_id=imageID, ingredients=form.ingredients.data)
        db.session.add(recipe)
        current_user.recipes = current_user.recipes + [recipe]
        db.session.commit()

    try:
        return render_template('create_recipe.html', form=form)
    except TemplateNotFound:
        abort(404)