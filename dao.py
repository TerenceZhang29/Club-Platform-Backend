from db import db, Club, Event

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
# Otherwise, serialized form of the club;
def get_club_by_id(id):
  club = Club.query.filter_by(id = id).first()
  if club is None:
    return None
  return club.serialize()

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


# -- Event methods -----------------------------------

# get all the clubs
# Return: a list of serialized clubs
def get_events():
  return [e.serialize() for e in Event.query.all()]


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