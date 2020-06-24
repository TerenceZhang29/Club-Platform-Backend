import json
from flask import Flask, request
from db import db, Club, Event
import dao

# define db filename
db_filename = "data.db"
app = Flask(__name__)

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

# --Club routes------

# get all clubs
@app.route("/")
@app.route("/clubs/")
def get_clubs():
  return success_response(dao.get_clubs())

# create a club
@app.route("/clubs/", methods = ["POST"])
def create_club():
  body = json.loads(request.data)
  name = body.get("name", "None")
  link = body.get("link", "None")
  industry = body.get("industry", "None")
  email = body.get("email", "None")
  phone = body.get("phone", "None")
  about = body.get("about", "None")
  location = body.get("location", "None")
  registered_users = body.get("registered_users", 0)
  club = dao.create_club(
    name = name, 
    link = link, 
    industry = industry, 
    email = email, 
    phone = phone, 
    about = about, 
    location = location, 
    registered_users = registered_users
  )
  return success_response(club, 201)

# get a club by id
@app.route("/club/<int:club_id>/")
def get_club_by_id(club_id):
  club = dao.get_club_by_id(club_id)
  if club is None:
    return failure_response("Club with id: " + str(club_id) + " not found !")
  return success_response(club)

# update a club by id
@app.route("/club/<int:club_id>/", methods = ["POST"])
def update_club_by_id(club_id):
  body = json.loads(request.data)
  club = dao.update_club_by_id(club_id, body)

  if club is None:
    return failure_response("Club with id: " + str(club_id) + " not found !")
  return success_response(club)

# --Event routes------

# get all events
@app.route("/events/")
def get_events():
  return success_response(dao.get_events())

# create a event
@app.route("/events/", methods = ["POST"])
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

# update a event by id
@app.route("/event/<int:event_id>/", methods = ["POST"])
def update_event_by_id(event_id):
  body = json.loads(request.data)
  event = dao.update_event_by_id(event_id, body)

  if event is None:
    return failure_response("Event with id: " + str(event_id) + " not found !")
  return success_response(event)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)