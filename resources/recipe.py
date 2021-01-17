from flask import request
from flask_restful import Resource, reqparse

from db import db
from models.ingredient import IngredientModel
from models.recipe import RecipeModel


class Recipe(Resource):

  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('search',
                        required=True,
                        help='This field cannot be left blank.')
    search = parser.parse_args()['search']

    recipes = RecipeModel.query.filter(RecipeModel.name.ilike('%{}%'.format(search)))

    return {'recipes': [recipe.json() for recipe in recipes]}

  def delete(self):
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id',
                        required=True,
                        help='This field cannot be left blank.')
    recipe_id = parser.parse_args()['recipe_id']

    recipe = RecipeModel.find_by_id(recipe_id)
    if (recipe): 
      for ingredient in recipe.ingredients.all():
        ingredient.delete_from_db()

      recipe.delete_from_db(commit=True)

      return "Successfully deleted recipe.", 200

    return "Error", 404
    

  def put(self):
    data = request.get_json(force=True)
    recipe_id = data['id']

    updated_r = {
      'uid': data['id'],
      'name': data['name'],
      'notes': data['notes'],
      'image_url': data['image_url'],
    }

    updated_i = [
      {
        'uid': ing['id'],
        'recipe_id': data['id'],
        'name': ing['name'],
        'measure': ing['quantity'],
      }
      for ing in data['ingredients']
    ]


    recipe = RecipeModel.find_by_id(recipe_id)
    if (recipe): 
      message = "Successfully edited recipe."

      for ing in recipe.ingredients.all():
        ing.delete_from_db()

      RecipeModel.find_by_id(recipe_id).update(**updated_r)
      db.session.commit()
    else: 
      message = "Successfully uploaded recipe."

      recipe = RecipeModel(**updated_r)
      recipe.save_to_db()

    for ingredient in updated_i:
        ing = IngredientModel(**ingredient)
        ing.save_to_db()

    return message, 200

