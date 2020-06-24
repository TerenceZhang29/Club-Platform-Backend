import json
from flask import Flask, request
from db import db, Club, User
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

# --Club routes------------------------------------------

# get all clubs
@app.route("/")
@app.route("/clubs/")
def get_clubs():
  return success_response(dao.get_clubs())

# create a club
@app.route("/clubs/", methods = ["POST"])
def create_club():
  body = json.loads(request.data)
  club = dao.create_club(body)
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

# --User routes------------------------------------------

# get all users
@app.route("/")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)