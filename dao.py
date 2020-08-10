from db import db, Club, Event, User
import json

# -- Club methods -----------------------------------

# get all the clubs
# Return: a list of serialized clubs
def get_clubs():
  return [t.serialize() for t in Club.query.all()]

# create a club
# Return: serialized form of the club
def create_club(body):
  club = Club(body)

  db.session.add(club)
  db.session.commit()
  return club.serialize()

# get a club by id
# Return: 
# None if the club doesn't exist;
# Otherwise, a list of serialized clubs;
def get_club_by_id(id):
  club = Club.query.filter_by(id = id).first()
  if club is None:
    return None
  return club.serialize()

# get all clubs by industry
# Return: 
# None if the industry does not have any avaliable clubs;
# Otherwise, serialized form of the clubs;
def get_clubs_by_industry(industry):
  clubs = Club.query.filter_by(industry = industry)
  if clubs is None:
    return None
  return [e.serialize() for e in clubs]

# get all clubs by registered users
# Return: 
# None if no club has this number of registered users;
# Otherwise, serialized form of the clubs;
def get_clubs_by_registered_users(min, max):
  clubs = Club.query.filter(max >= Club.registered_users, min <= Club.registered_users)
  if clubs is None:
    return None
  return [e.serialize() for e in clubs]


# update a club by id
# Return:
# None if the club doesn't exist
# Otherwise, the serialized form of the updated club
def update_club_by_id(id, body):
  club = Club.query.filter_by(id = id).first()
  if club is None:
    return None
  
  club.name = body.get("name", club.name)
  club.link = body.get("link", club.link)
  club.industry = body.get("industry", club.industry)
  if body.get("email") is not None:
    club.email = body.get("email")
  if body.get("phone") is not None:
    club.phone = body.get("phone", club.phone)
  club.about = body.get("about", club.about)
  club.location = body.get("location", club.location)
  club.registered_users = body.get("registered_users", club.registered_users)
  db.session.commit()
  return club.serialize()

def get_most_interested_clubs():
  clubs = Club.query.order_by(Club.subscribers.desc()).limit(5)
  if clubs is None:
    return None
  return [e.serialize() for e in clubs]

def desc_clubs():
  clubs = Club.query.order_by(Club.subscribers.desc())
  if clubs is None:
    return None
  return [e.serialize() for e in clubs]

# -- User methods -----------------------------------

# get all the users
# Return:
# a list of all users in serialized form
def get_users():
  return [u.serialize() for u in User.query.all()]

# get the user with given user id
# Return:
# serialized form of the user
# None if the user does not exist
def get_user_by_id(user_id):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  
  return user.serialize()

# create a user with given json
# Return:
# serialized form of the created user
def create_user(body):
  user = User(body)

  db.session.add(user)
  db.session.commit()
  return user.serialize()

# update a user with given user id and json
# Return:
# serialized form of the updated user
# None if the user does not exist
def update_user_by_id(user_id, body):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  
  user.name = body.get("name", user.name)
  user.major = body.get("major", user.major)
  user.secondary_major = body.get("secondary_major", user.secondary_major)
  user.industry = body.get("industry", user.industry)
  db.session.commit()
  return user.serialize()

# delete the user with given user id
# Return:
# serialized form of the user deleted
# None if the user does not exist
def delete_user_by_id(user_id):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None

  db.session.delete(user)
  db.session.commit()
  return user.serialize()

# -- Club-User association methods -----------------------------------

# add a member to the club
# Return:
# the serialized form of the member
# None if the club/user does not exist
def add_member_to_club(club_id, user_id):
  club = Club.query.filter_by(id = club_id).first()
  if club is None:
    return None
  
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  
  club.members.append(user)
  user.your_clubs.append(club)

  db.session.commit()
  return user.serialize()

# delete a member from the club
# Return:
# the serialized form of the deleted member
# None if the club/user does not exist
# None if the user is not a member of the club
def delete_member_from_club(club_id, user_id):
  club = Club.query.filter_by(id = club_id).first()
  if club is None:
    return None
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None

  if (user not in club.members) or (club not in user.your_clubs) :
    return None

  club.members.remove(user)
  db.session.commit()
  return user.serialize()

# add a user to subscribe the club
# Return:
# The serialized form of the user
# None if the club/user does not exist
def add_subscriber_to_club(club_id,user_id):
  club = Club.query.filter_by(id = club_id).first()
  if club is None:
    return None
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None

  club.subscribers.append(user)
  user.subscribed_clubs.append(club)

  db.session.commit()
  return user.serialize()

# delete a subscriber from the club
# Return:
# The serialized form of the subscriber
# None if the club/user does not exist
# None if the user is not a subscriber of the club
def delete_subscriber_from_club(club_id, user_id):
  club = Club.query.filter_by(id = club_id).first()
  if club is None:
    return None
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  
  if (user not in club.subscribers) or (club not in user.subscribed_clubs):
    return None
  
  club.subscribers.remove(user)
  db.session.commit()
  return user.serialize()

def get_your_clubs(user_id):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  return user.your_clubs

def get_subscribed_clubs(user_id):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  return user.subscribed_clubs

# -- Event methods -----------------------------------

# get all the clubs
# Return: a list of serialized clubs
def get_events():
    return [t.serialize() for t in Event.query.all()]

# create a event
# Return: serialized form of the event
def create_event(name, club_id, time, description, link, industry, location, registered_users):
  event= Event(
    name = name,
    club_id = club_id,
    time = time,
    description = description,
    link = link, 
    industry = industry,
    location = location,
    registered_users = registered_users
  )

  db.session.add(event)
  db.session.commit()
  return event.serialize()

# get a event by id
# Return: 
# None if the event doesn't exist;
# Otherwise, serialized form of the event;
def get_event_by_id(id):
  event = Event.query.filter_by(id = id).first()
  if event is None:
    return None
  return event.serialize()

# get all events by club_id
# Return: 
# None if the club doesn't exist or the club does not have any avaliable events;
# Otherwise, serialized form of the events;
def get_events_by_club_id(club_id):
  events = Event.query.filter_by(club_id = club_id)
  if events is None:
    return None
  return [e.serialize() for e in events]

# get all events by industry
# Return: 
# None if the industry does not have any avaliable events;
# Otherwise, serialized form of the events;
def get_events_by_industry(industry):
  events = Event.query.filter_by(industry = industry)
  if events is None:
    return None
  return [e.serialize() for e in events]

# get all events by registered users
# Return: 
# None if no event has this number of registered users;
# Otherwise, serialized form of the events;
def get_events_by_registered_users(min, max):
  events = Event.query.filter(max >= Event.registered_users, min <= Event.registered_users)
  if events is None:
    return None
  return [e.serialize() for e in events]

# update a event by id
# Return:
# None if the event doesn't exist
# Otherwise, the serialized form of the updated event
def update_event_by_id(id, body):
  event = Event.query.filter_by(id = id).first()
  if event is None:
    return None
  
  event.name = body.get("name", event.name)
  event.club_id = body.get("club_id", event.club_id)
  event.time = body.get("time", event.time)
  event.description = body.get("description", event.description)
  event.link = body.get("link", event.link)
  event.industry = body.get("industry", event.industry)
  event.location = body.get("location", event.location)
  event.registered_users = body.get("registered_users", event.registered_users)
  db.session.commit()
  return event.serialize()

def get_most_interested_events():
  events = Event.query.order_by(Event.registered_users.desc()).limit(5)
  if events is None:
    return None
  return [e.serialize() for e in events]

def desc_events():
  events = Event.query.order_by(Event.registered_users.desc())
  if events is None:
    return None
  return [e.serialize() for e in events]

# delete a event by id
# Return:
# None if the event doesn't exist
# Otherwise, the seriailized form of the deleted event
def delete_event_by_id(id):
  event = Event.query.filter_by(id=id).first()
  if event is None:
    return None

  db.session.delete(event)
  db.session.commit()
  return event.serialize()

# -- Event-User association methods -----------------------------------

# add a register to an event
# Return:
# the serialized form of registers
# None if the event/user does not exist
def add_register_to_event(event_id, user_id):
  event = Event.query.filter_by(id = event_id).first()
  if event is None:
    return None
  
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None

  event.registers.append(user)
  user.registered_events.append(event)

  db.session.commit()
  return user.serialize()

# delete a register from the event
# Return:
# the serialized form of the deleted register
# None if the event/user does not exist
# None if the user is not a of the event
def delete_register_from_event(event_id, user_id):
  event = Event.query.filter_by(id = event_id).first()
  if event is None:
    return None
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None

  if (user not in event.registers) or (club not in user.registered_events) :
    return None

  event.registers.remove(user)
  db.session.commit()
  return user.serialize()

def get_registered_events(user_id):
  user = User.query.filter_by(id = user_id).first()
  if user is None:
    return None
  return user.registered_events
