from db import db, Club

# -- Club methods -----------------------------------

# get all the clubs
# Return: a list of serialized clubs
def get_clubs():
  return [t.serialize() for t in Club.query.all()]


# create a club
# Return: serialized form of the club
# def create_club(name, link, industry, email, phone, about, location, registered_users):
#   club = Club(
#     name = name,
#     link = link, 
#     industry = industry,
#     email = email,
#     phone = phone,
#     about = about, 
#     location = location,
#     registered_users = registered_users
#   )

#   db.session.add(club)
#   db.session.commit()
#   return club.serialize()
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