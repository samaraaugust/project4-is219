from flask import Blueprint, render_template,current_app,abort, flash, Request, Response, url_for
from flask_login import login_required, current_user
from app.recipes.forms import new_recipe, edit_recipe, search_food
from app.db.models import Recipes, Image, User
from jinja2 import TemplateNotFound
from app.db import db
from base64 import b64encode
from werkzeug.utils import secure_filename, redirect
recipes = Blueprint('recipes', __name__,
                        template_folder='templates')
"""
@recipes.route('/<int:id>', methods=['GET'])
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return "no image with is", 404
    return Response(img.img, mimetype=img.mimetype)
"""
@recipes.route('/recipes/search', methods=['GET', 'POST'])
@login_required
def search_for_recipes():
    food_api_key = current_app.config.get('FOOD_API_KEY')
    form = search_food()
    if form.validate_on_submit():
        search_value = form.search.data
        return render_template('browse_search.html', food_api_key=food_api_key,
                               search_value=search_value)
    try:
        return render_template('search_api_recipes.html', form=form)
    except TemplateNotFound:
        abort(404)

@recipes.route('/recipes/<int:recipe_id>/delete', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe Deleted', 'success')
    return redirect(url_for('recipes.users_recipes'), 302)


@recipes.route('/recipes/<int:recipe_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_new_recipe(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    form = edit_recipe(obj=recipe)
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        mimetype = form.image.data.mimetype
        image2 = Image(img=form.image.data.read(), name=filename, mimetype=mimetype)
        db.session.add(image2)
        db.session.commit()
        imageID = image2.id
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.image_id = image2.id
        recipe.ingredients = form.ingredients.data
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe Edited Successfully', 'success')
        return redirect(url_for('recipes.users_recipes'))
    return render_template('edit_recipe.html', form=form)

@recipes.route('/recipes/users', methods=['POST', 'GET'])
@login_required
def users_recipes():
    idNum = User.get_id(current_user)
    data = Recipes.query.filter_by(user_id=idNum)
    overall = []
    for p in data:
        sep = []
        sep.append(p)
        imageID = p.image_id
        userID = p.user_id
        userData = User.query.filter_by(id=userID).first()
        sep.append(userData)
        imageData = Image.query.filter_by(id=imageID).first()
        pic = imageData.img
        newImg = b64encode(pic).decode("utf-8")
        sep.append(newImg)
        overall.append(sep)
    try:
        return render_template('users_recipes.html', overall=overall)
    except TemplateNotFound:
        abort(404)

@recipes.route('/recipes/<int:recipe_id>', methods=['POST', 'GET'])
@login_required
def one_recipe(recipe_id):
    data = Recipes.query.filter_by(id=recipe_id).first()
    overall = []
    sep = []
    sep.append(data)
    imageID = data.image_id
    userID = data.user_id
    userData = User.query.filter_by(id=userID).first()
    sep.append(userData)
    imageData = Image.query.filter_by(id=imageID).first()
    pic = imageData.img
    newImg = b64encode(pic).decode("utf-8")
    sep.append(newImg)
    overall.append(sep)
    return render_template('seperate_recipe.html', overall=overall)

@recipes.route('/recipes', methods=['POST', 'GET'])
@login_required
def browse_all_recipes():
    data = Recipes.query.all()
    overall = []
    for p in data:
        sep = []
        sep.append(p)
        imageID = p.image_id
        userID = p.user_id
        userData = User.query.filter_by(id=userID).first()
        sep.append(userData)
        imageData = Image.query.filter_by(id=imageID).first()
        pic = imageData.img
        newImg = b64encode(pic).decode("utf-8")
        sep.append(newImg)
        overall.append(sep)
    """
    image_data = Image.query.all()
    list_info = []
    for i in image_data:
        pic = i.img
        newImg2 = b64encode(pic).decode("utf-8")
        list_info.append(newImg2)
    """
    try:
        return render_template('browse_all_recipes.html', overall=overall)
    except TemplateNotFound:
        abort(404)



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

        return redirect(url_for('recipes.browse_all_recipes'))

    try:
        return render_template('create_recipe.html', form=form)
    except TemplateNotFound:
        abort(404)