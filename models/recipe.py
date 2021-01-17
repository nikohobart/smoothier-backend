from db import db

state = 'hi'

class RecipeModel(db.Model):
  __tablename__ = 'recipe'

  uid = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  notes = db.Column(db.Text())
  image_url = db.Column(db.String(600))

  ingredients = db.relationship('IngredientModel', lazy='dynamic')

  def __init__(self, uid, name, notes, image_url):
    self.uid = uid
    self.name = name
    self.notes = notes
    self.image_url = image_url

  def json(self):
    return {
      'recipe_id': self.uid,
      'name': self.name,
      'notes': self.notes,
      'image_url': self.image_url,
      'ingredients': [ing.json() for ing in self.ingredients.all()],
    }

  def update(self, uid, name, notes, image_url):
    self.uid = uid
    self.name = name
    self.notes = notes
    self.image_url = image_url
    db.session.commit()

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: db.session.commit()

  def delete_from_db(self, commit=False):
    db.session.delete(self)
    if commit: db.session.commit()

  @classmethod
  def find_by_id(cls, id):
      """Return recipe from database with recipe_id id."""
      return cls.query.filter_by(uid=id).first()
