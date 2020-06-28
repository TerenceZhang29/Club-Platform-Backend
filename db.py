from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# clubs to events many-to-many relationship
clubs_to_events_table = db.Table("clubs_to_events", db.Model.metadata,
  db.Column("club_id", db.Integer, db.ForeignKey('club.id')),
  db.Column("event_id", db.Integer, db.ForeignKey('event.id'))
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
  events = db.relationship('Event', secondary = clubs_to_events_table, 
    backp_poplulates = 'clubs')

  def __init__(self, **kwargs):
    self.name = kwargs.get("name", "None")
    self.link = kwargs.get("link", "None")
    self.industry = kwargs.get("industry", "None")
    self.email = kwargs.get("email", "None")
    self.phone = kwargs.get("phone", "None")
    self.about = kwargs.get("about", "None")
    self.location = kwargs.get("location", "None")
    self.registered_users = kwargs.get("registered_users", 0)

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "link": self.industry,
      "email": self.email,
      "phone": self.phone,
      "about": self.about,
      "location": self.location,
      "registered_users": self.registered_users,
      "events" = [e.serialize() for e in self.events]
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
  clubs = db.relationship('Club', secondary = clubs_to_events_table, 
    backp_poplulates = 'events')

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
      "clubs" = [c.serialize() for c in self.clubs]
    }


