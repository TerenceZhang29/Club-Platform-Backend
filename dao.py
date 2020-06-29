from db import db, Club, User

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
  club.email = body.get("email", club.email)
  club.phone = body.get("phone", club.phone)
  club.about = body.get("about", club.about)
  club.location = body.get("location", club.location)
  club.registered_users = body.get("registered_users", club.registered_users)
  db.session.commit()
  return club.serialize()

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