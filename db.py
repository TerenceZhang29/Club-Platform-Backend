from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

# Class for clubs
# Parameters:
# id: club id
# name: club name
# link: website link
# industry: club industry
# email: club email
# phone: club phone
# about: club about info
# location: club location
# registered_users: number of students who registered this club
class Club(db.Model):
  __tablename__ = "clubs"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.Text, nullable = False)
  link = db.Column(db.Text, nullable = False)
  industry = db.Column(db.Text, nullable = False)
  email = db.Column(db.Text, nullable = False)
  phone = db.Column(db.Text, nullable = False)
  about = db.Column(db.Text, nullable = False)
  location = db.Column(db.Text, nullable = False)
  registered_users = db.Column(db.Integer, nullable = False)

  def __init__(self, body):
    self.name = body.get("name", "None")
    self.link = body.get("link", "None")
    self.industry = body.get("industry", "None")
    self.email = body.get("email", "None")
    self.phone = body.get("phone", "None")
    self.about = body.get("about", "None")
    self.location = body.get("location", "None")
    self.registered_users = body.get("registered_users", 0)

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "link": self.link,
      "industry": self.industry,
      "email": self.email,
      "phone": self.phone,
      "about": self.about,
      "location": self.location,
      "registered_users": self.registered_users
    }