import json
from flask import Flask, request
from db import db, Club
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
@app.route("/api/clubs/")
def get_clubs():
  return success_response(dao.get_clubs())

# create a club
@app.route("/api/clubs/", methods = ["POST"])
# def create_club():
#   body = json.loads(request.data)
#   name = body.get("name", "None")
#   link = body.get("link", "None")
#   industry = body.get("industry", "None")
#   email = body.get("email")
#   phone = body.get("phone")
#   about = body.get("about", "None")
#   location = body.get("location", "None")
#   registered_users = body.get("registered_users", 0)
#   club = dao.create_club(
#     name = name, 
#     link = link, 
#     industry = industry, 
#     email = email, 
#     phone = phone, 
#     about = about, 
#     location = location, 
#     registered_users = registered_users
#   )
#   return success_response(club, 201)
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

# update a club by id
@app.route("/api/club/<int:club_id>/", methods = ["POST"])
def update_club_by_id(club_id):
  body = json.loads(request.data)
  club = dao.update_club_by_id(club_id, body)

  if club is None:
    return failure_response("Club with id: " + str(club_id) + " not found !")
  return success_response(club)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)