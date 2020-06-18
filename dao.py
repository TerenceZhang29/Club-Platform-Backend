from db import db, Club

# -- Club methods -----------------------------------
def get_clubs():
  return [t.serialize() for t in Club.query.all()]

def create_club(name, link, industry, email, phone, about, location, registered_users):
  club = Club(
    name = name,
    link = link, 
    industry = industry,
    email = email,
    phone = phone,
    about = about, 
    location = location,
    registered_users = registered_users
  )

  db.session.add(club)
  db.session.commit()
  return club.serialize()