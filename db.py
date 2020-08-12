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

# association table of registers and events
event_users = db.Table(
  "event_users",
  db.Model.metadata,
  db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
  db.Column("event_id", db.Integer, db.ForeignKey("events.id"))
) 

# association table of subscribers and clubs
subscribed_club_users = db.Table(
  "subscribed_club_users",
  db.Model.metadata,
  db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
  db.Column("club_id", db.Integer, db.ForeignKey("clubs.id"))
) 

# clubs to events many-to-many relationship
clubs_to_events_table = db.Table("clubs_to_events", db.Model.metadata,
  db.Column("club_id", db.Integer, db.ForeignKey('clubs.id')),
  db.Column("event_id", db.Integer, db.ForeignKey('events.id'))
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
  name = db.Column(db.Text, nullable = False)
  link = db.Column(db.Text, nullable = False)
  industry = db.Column(db.Text, nullable = False)
  email = db.Column(db.Text, nullable = False)
  phone = db.Column(db.Text, nullable = False)
  about = db.Column(db.Text, nullable = False)
  location = db.Column(db.Text, nullable = False)
  registered_users = db.Column(db.Integer, nullable = False)
  
  members = db.relationship("User", secondary = your_club_users, back_populates = "your_clubs")
  subscribers = db.relationship("User", secondary = subscribed_club_users, back_populates = "subscribed_clubs")
  
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
      "registered_users": self.registered_users,
      "members": [m.id for m in self.members],
      "subscribers": [s.id for s in self.subscribers]
    }

# Class for events
# Parameters:
# id: event id (INTEGER)
# name: event name (TEXT)
# club_id: id of the club holding the event (INTEGER)
# time: event time (TEXT) 
# description: description of the event (TEXT)
# link: event link (TEXT)
# industry: event industry (Text)
# location: event location (Text)
# registed_users: number of students who registered for this event (INTEGER)
class Event(db.Model):
  __tablename__= "events"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.Text, nullable = False)
  club_id = db.Column(db.Integer, nullable = False)
  time = db.Column(db.Text, nullable = False)
  description = db.Column(db.Text, nullable = False)
  link = db.Column(db.Text, nullable = False)
  industry = db.Column(db.Text, nullable = False)
  location = db.Column(db.Text, nullable = False)
  registered_users = db.Column(db.Integer, nullable = False)

  registers = db.relationship("User", secondary = event_users, back_populates = "registered_events")

  def __init__(self, **kwargs):
    self.name = kwargs.get("name", "None")
    self.club_id = kwargs.get("club_id", 0)
    self.time = kwargs.get("time", "None")
    self.description = kwargs.get("description", "None")
    self.link = kwargs.get("link", "None")
    self.industry = kwargs.get("industry", "None")
    self.location = kwargs.get("location", "None")
    self.registered_users = kwargs.get("registered_users", 0)

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "club_id": self.club_id,
      "time": self.time,
      "description": self.description,
      "link": self.link,
      "industry": self.industry,
      "location": self.location,
      "registered_users": self.registered_users,
      "registers": [r.id for m in self.registers]
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
  registerd_events = db.relationship("Event", secondary = event_users, back_populates = "registers")

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
      "subscribed_clubs": [s.id for s in self.subscribed_clubs],
      "registered_events": [r.id for r in self.registered_events]
    }


