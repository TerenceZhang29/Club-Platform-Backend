import json
from flask import Flask, request
from db import db, Club, Event, User
from flask_cors import CORS
import dao

# define db filename
db_filename = "data.db"
app = Flask(__name__)
CORS(app)

# setup config
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# --Club routes------------------------------------------

# get all clubs
@app.route("/api/clubs/")
def get_clubs():
  return success_response(dao.get_clubs())

# create a club
@app.route("/api/clubs/", methods = ["POST"])
def create_club():
  body = json.loads(request.data)
  club = dao.create_club(body)
  return success_response(club, 201)

# get a club by id
@app.route("/api/club/<int:club_id>/")
def get_club_by_id(club_id):
  club = dao.get_club_by_id(club_id)
  if club is None:
    return failure_response("Club with id: " + str(club_id) + " not found !")
  return success_response(club)

# get all clubs by industry
@app.route("/api/clubs/<string:industry>/")
def get_clubs_by_industry(industry):
  clubs = dao.get_clubs_by_industry(industry)
  if clubs is None:
    return failure_response(industry + "industry does not have any clubs !")
  return success_response(clubs)

# get all clubs by registered users
@app.route("/api/clubs/<int:min>/<int:max>/")
def get_clubs_by_registered_users(min, max):
  clubs = dao.get_clubs_by_registered_users(min, max)
  if clubs is None:
    return failure_response("no clubs have registered users between " + str(min) + " to " + str(max) + " !")
  return success_response(clubs)

# get all clubs ordered by subscribers
@app.route("/api/clubs/desc/")
def desc_clubs():
  clubs = dao.desc_clubs()
  if clubs is None:
    return failure_response("no clubs")
  return success_response(clubs)

# update a club by id
@app.route("/api/club/<int:club_id>/", methods = ["POST"])
def update_club_by_id(club_id):
  body = json.loads(request.data)
  club = dao.update_club_by_id(club_id, body)

  if club is None:
    return failure_response("Club with id: " + str(club_id) + " not found !")
  return success_response(club)

# --User routes------------------------------------------

# get all users
@app.route("/api/users/")
def get_users():
  return success_response(dao.get_users())

# create a user
@app.route("/api/users/", methods = ["POST"])
def create_user():
  body = json.loads(request.data)
  user = dao.create_user(body)
  return success_response(user, 201)

# get the user by id
@app.route("/api/user/<int:user_id>/")
def get_user_by_id(user_id):
  user = dao.get_user_by_id(user_id)
  if user is None:
    return failure_response("User with id: " + str(user_id) + " not found!")
  return success_response(user)

# update the user by id
@app.route("/api/user/<int:user_id>/", methods = ["POST"])
def update_user_by_id(user_id):
  body = json.loads(request.data)
  user = dao.update_user_by_id(user_id, body)

  if user is None:
    return failure_response("User with id: " + str(user_id) + " not found!")
  return success_response(user)

# delete the user by id
@app.route("/api/user/<int:user_id>/", methods = ["DELETE"])
def delete_user_by_id(user_id):
  user = dao.delete_user_by_id(user_id)

  if user is None:
    return failure_response("User with id: " + str(user_id) + " not found!")
  return success_response(user)

# --Club-User routes------------------------------------------

# add a member to the club
@app.route("/api/member/club/<int:club_id>/user/<int:user_id>/", methods = ["POST"])
def add_member_to_club(club_id, user_id):
  added_user = dao.add_member_to_club(club_id,user_id)

  if added_user is None:
    return failure_response("Addition failed!")
  return success_response(added_user)

# delete a member from the club
@app.route("/api/member/club/<int:club_id>/user/<int:user_id>/", methods = ["DELETE"])
def delete_member_from_club(club_id, user_id):
  deleted_user = dao.delete_member_from_club(club_id,user_id)

  if deleted_user is None:
    return failure_response("Deletion failed!")
  return success_response(deleted_user)

# add a subscriber to the club
@app.route("/api/subscribe/club/<int:club_id>/user/<int:user_id>/", methods = ["POST"])
def add_subscriber_to_club(club_id, user_id):
  added_subscriber = dao.add_subscriber_to_club(club_id,user_id)

  if added_subscriber is None:
    return failure_response("Subscribition failed!")
  return success_response(added_subscriber)

# delete a subscriber from the club
@app.route("/api/subscribe/club/<int:club_id>/user/<int:user_id>/", methods = ["DELETE"])
def delete_subscriber_from_club(club_id, user_id):
  deleted_subscriber = dao.delete_subscriber_from_club(club_id, user_id)

  if deleted_subscriber is None:
    return failure_response("Deletion failed!")
  return success_response(deleted_subscriber)

# --Event routes------

# get all events
@app.route("/api/events/")
def get_events():
  print("RICHIE FUCK")
  return success_response(dao.get_events(), 200)

# create a event
@app.route("/api/events/", methods = ["POST"])
def create_event():
  body = json.loads(request.data)
  name = body.get("name", "None")
  club_id = body.get("club_id", 0)
  time = body.get("time", "None")
  description = body.get("description", "None")
  link = body.get("link", "None")
  industry = body.get("industry", "None")
  location = body.get("location", "None")
  registered_users = body.get("registered_users", 0)
  event = dao.create_event(
    name = name, 
    club_id = club_id,
    time = time,
    description = description,
    link = link, 
    industry = industry, 
    location = location, 
    registered_users = registered_users
  )
  return success_response(event, 201)

# get a event by id
@app.route("/event/<int:event_id>/")
def get_event_by_id(event_id):
  event = dao.get_event_by_id(event_id)
  if event is None:
    return failure_response("Event with id: " + str(event_id) + " not found !")
  return success_response(event)

# get all events by club_id
@app.route("/events/<int:club_id>/")
def get_events_by_club_id(club_id):
  events = dao.get_events_by_club_id(club_id)
  if events is None:
    club = dao.get_club_by_id(club_id)
    if club is None:
      return failure_response("Club with id: " + str(club_id) + " not found !")
    return failure_response("Club with id: " + str(club_id) + "does not have any events !")
  return success_response(events)

# get all events by industry
@app.route("/events/<string:industry>/")
def get_events_by_industry(industry):
  events = dao.get_events_by_industry(industry)
  if events is None:
    return failure_response(industry + "industry does not have any events !")
  return success_response(events)

# get all events by registered users
@app.route("/events/<int:min>/<int:max>/")
def get_events_by_registered_users(min, max):
  events = dao.get_events_by_registered_users(min, max)
  if events is None:
    return failure_response("no events have registered users between " + str(min) + " to " + str(max) + " !")
  return success_response(events)

# get all events ordered by registers
@app.route("/api/events/desc/")
def desc_events():
  events = dao.desc_events()
  if events is None:
    return failure_response("no events")
  return success_response(events)

# update a event by id
@app.route("/event/<int:event_id>/", methods = ["POST"])
def update_event_by_id(event_id):
  body = json.loads(request.data)
  event = dao.update_event_by_id(event_id, body)

  if event is None:
    return failure_response("Event with id: " + str(event_id) + " not found !")
  return success_response(event)

# delete a event by id
@app.route("/event/<int:event_id>/", methods = ["DELETE"])
def delete_event_by_id(event_id):
  event = dao.delete_event_by_id(event_id)

  if event is None:
    return failure_response("Event with id: " + str(event_id) + " not found !")
  return success_response(event)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)