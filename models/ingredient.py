from db import db


class IngredientModel(db.Model):
  __tablename__ = 'ingredient'

  uid = db.Column(db.Integer, primary_key=True)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.uid'), primary_key=True)
  name = db.Column(db.String(50))
  measure = db.Column(db.String(30))

  recipe = db.relationship('RecipeModel')

  def json(self):
    return {
      'ingredient_id': self.uid,
      'name': self.name,
      'measure': self.measure,
    }

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: db.session.commit()

  def delete_from_db(self, commit=False):
    db.session.delete(self)
    db.session.commit()