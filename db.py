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
#
# The null values are filled in with default values 
# Default value for Text is "None"
# Default value for Integer is 0
class Club(db.Model):
  __tablename__ = "clubs"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  link = db.Column(db.String, nullable = False)
  industry = db.Column(db.String, nullable = False)
  email = db.Column(db.String, nullable = False)
  phone = db.Column(db.String, nullable = False)
  about = db.Column(db.Text, nullable = False)
  location = db.Column(db.String, nullable = False)
  registered_users = db.Column(db.Integer, nullable = False)

  # init for class Club
  def __init__(self, **kwargs):
    self.name = kwargs.get("name", "None")
    self.link = kwargs.get("link", "None")
    self.industry = kwargs.get("industry", "None")
    self.email = kwargs.get("email", "None")
    self.phone = kwargs.get("phone", "None")
    self.about = kwargs.get("about", "None")
    self.location = kwargs.get("location", "None")
    self.registered_users = kwargs.get("registered_users", 0)

  # Return:
  # serialuzed json of club
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
  
  # Class for users
  # Parameters:
  # id: user id
  # name: user name
  # major: user major
  # secondary_major: user secondary major; "None" if not available
  # industry: user industry
  class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)
    major = db.Column(db.Text, nullable = False)
    secondary_major = db.Column(db.Text, nullable = False)
    industry = db.Column(db.Text, nullable = False)

    # init for class User
    def __init__(self, body):
