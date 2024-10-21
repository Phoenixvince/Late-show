from models import db, Guest,Episode,Appearance
from app import app

# guests=[{
#   "id": 1,
#   "name": "Reg Sutty",
#   "occupation": "doctor"
# }, {
#   "id": 2,
#   "name": "Maury Malsher",
#   "occupation": "scientist"
# }, {
#   "id": 3,
#   "name": "Wendell Braidon",
#   "occupation": "police officer"
# }, {
#   "id": 4,
#   "name": "Fitzgerald Skrine",
#   "occupation": "actor"
# }, {
#   "id": 5,
#   "name": "Lesya McClarence",
#   "occupation": "artist"
# }, {
#   "id": 6,
#   "name": "Ardella Brickwood",
#   "occupation": "firefighter"
# }, {
#   "id": 7,
#   "name": "Gare Blanchflower",
#   "occupation": "teacher"
# }, {
#   "id": 8,
#   "name": "Andromache Jewer",
#   "occupation": "teacher"
# }, {
#   "id": 9,
#   "name": "Opaline Apark",
#   "occupation": "engineer"
# }, {
#   "id": 10,
#   "name": "Yvette Danilchik",
#   "occupation": "engineer"
# }]
# with app.app_context():
#     db.session.add_all([Guest(**guest) for guest in guests])
#     db.session.commit()

# episodes=[{
#   "id": 1,
#   "date": "10/19/2024",
#   "number": 2
# }, {
#   "id": 2,
#   "date": "7/7/2024",
#   "number": 2
# }, {
#   "id": 3,
#   "date": "11/20/2023",
#   "number": 3
# }, {
#   "id": 4,
#   "date": "6/11/2024",
#   "number": 6
# }, {
#   "id": 5,
#   "date": "7/30/2024",
#   "number": 2
# }, {
#   "id": 6,
#   "date": "7/7/2024",
#   "number": 4
# }, {
#   "id": 7,
#   "date": "12/6/2023",
#   "number": 4
# }, {
#   "id": 8,
#   "date": "2/22/2024",
#   "number": 3
# }, {
#   "id": 9,
#   "date": "6/20/2024",
#   "number": 2
# }, {
#   "id": 10,
#   "date": "3/13/2024",
#   "number": 1
# }]

# with app.app_context():
#     db.session.add_all([Episode(**episode) for episode in episodes])
#     db.session.commit()

appearances=[{
  "rating": 3,
  "guest_id": 1,
  "episode_id": 5
}, {
  "rating": 4,
  "guest_id": 9,
  "episode_id": 7
}, {
  "rating": 2,
  "guest_id": 8,
  "episode_id": 6
}, {
  "rating": 2,
  "guest_id": 10,
  "episode_id": 7
}, {
  "rating": 5,
  "guest_id": 4,
  "episode_id": 5
}, {
  "rating": 2,
  "guest_id": 6,
  "episode_id": 9
}, {
  "rating": 3,
  "guest_id": 8,
  "episode_id": 2
}, {
  "rating": 1,
  "guest_id": 6,
  "episode_id": 3
}, {
  "rating": 1,
  "guest_id": 1,
  "episode_id": 6
}, {
  "rating": 2,
  "guest_id": 3,
  "episode_id": 4
}]
with app.app_context():
    db.session.add_all([Appearance(**appearance) for appearance in appearances])
    db.session.commit()