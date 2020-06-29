from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

# association table of members and clubs
your_club_users = db.Table(
  "your_club_users",
  db.Model.metadata,
  db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
  db.Column("club_id", db.Integer, db.ForeignKey("clubs.id"))
) 

# association table of subscribers and clubs
subscribed_club_users = db.Table(
  "subscribed_club_users",
  db.Model.metadata,
  db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
  db.Column("club_id", db.Integer, db.ForeignKey("clubs.id"))
) 

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

  members = db.relationship("User", secondary = your_club_users, back_populates = "your_clubs")
  subscribers = db.relationship("User", secondary = subscribed_club_users, back_populates = "subscribed_clubs")

  # init for class Club
  def __init__(self, body):
    self.name = body.get("name", "None")
    self.link = body.get("link", "None")
    self.industry = body.get("industry", "None")
    self.email = body.get("email", "None")
    self.phone = body.get("phone", "None")
    self.about = body.get("about", "None")
    self.location = body.get("location", "None")
    self.registered_users = body.get("registered_users", 0)

  # serialize method for Club
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
      "registered_users": self.registered_users,
      "members": [m.id for m in self.members],
      "subscribers": [s.id for s in self.subscribers]
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

  your_clubs = db.relationship("Club", secondary = your_club_users, back_populates = "members" )
  subscribed_clubs = db.relationship("Club", secondary = subscribed_club_users, back_populates = "subscribers" )

  # init for class User
  def __init__(self, body):
    self.name = body.get("name", "None")
    self.major = body.get("major", "None")
    self.secondary_major = body.get("secondary_major", "None")
    self.industry = body.get("industry", "None")
  
  # serialize method for User
  # Return:
  # serialuzed json of user
  # includes the list of clubs the users are member
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "major": self.major,
      "secondary_major": self.secondary_major,
      "industry": self.industry,
      "your_clubs": [c.id for c in self.your_clubs],
      "subscribed_clubs": [s.id for s in self.subscribed_clubs]
    }


