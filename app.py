from flask import Flask,request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from models import db, Episode, Guest, Appearance
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///lateshows.db'
migrate=Migrate(app, db)
db.init_app(app)
api=Api(app)
ma=Marshmallow(app)


def validate_duration(value):
    if value <= 0:
        raise ValidationError('Duration must be a positive number.')

def validate_rating(value):
    if value < 1 or value > 5:
        raise ValidationError('Rating must be between 1 and 5.')
    

class EpisodeSchema(Schema):
    id = fields.Int(dump_only=True)  # Read-only field (auto-generated)
    title = fields.String(required=True, validate=lambda t: len(t) >= 5)
    duration = fields.Float(required=True, validate=validate_duration)
    date = fields.String(required=True)

# Schema for Guest
class GuestSchema(Schema):
    id = fields.Int(dump_only=True)  # Read-only field
    name = fields.String(required=True, validate=lambda n: len(n) > 0)
    rating = fields.Float(required=True, validate=validate_rating)
 

# Schema for Appearance
class AppearanceSchema(Schema):
    id = fields.Int(dump_only=True)  # Read-only field
    episode_id = fields.Int(required=True)
    guest_id = fields.Int(required=True)


# Nested fields for relationships
guest = fields.Nested(GuestSchema, required=True)  # Optional to include full details of guest
episode = fields.Nested(EpisodeSchema, required=True)  

# post_args = reqparse.RequestParser(bundle_errors=True)
# post_args.add_argument('appearnce_id', type=int, help='Error!! Add Id of the Appearance')
# post_args.add_argument('appearance_rating', type=int, help='Error!!! Add Rating of the Appearance')
# post_args.add_argument('appeance_episode', type=int, help='Error!!! Add Episode of the Appearance')
post_args = reqparse.RequestParser(bundle_errors=True)
post_args.add_argument('appearance_id', type=int, required=True, help='Error! Please provide the ID of the Appearance.')
post_args.add_argument('appearance_rating', type=int, required=True, help='Error! Please provide the rating for the Appearance.')
post_args.add_argument('appearance_episode', type=int, required=True, help='Error! Please provide the episode ID for the Appearance.')




@app.route('/')
def index():
    return f"<h1>Welcome to Phoenix Late-show API back-end development</h1>"
    
class EpisodeResource(Resource):
    def get (self):
        episodes=Episode.query.all()
        response=[episode.to_dict(rules=('-appearances',)) for episode in episodes]
        return response
    
class EpisodeById(Resource):
    def get(self, id):
        episode = Episode.query.get(id)  

        if episode is None:
            return {'error': 'Episode not found'}, 404 
        return episode.to_dict(), 200  
  
class GuestResource(Resource):
    def get (self):
        guests=Guest.query.all()
        response=[guest.to_dict(rules=('-appearances',)) for guest in guests]
        return response

class AppearanceResource(Resource):
    def post(self):
        try:
        
            data = request.get_json()

            if not data:
                return {'errors': ['No input data provided']}, 400

            rating = data.get('rating')
            episode_id = data.get('episode_id')
            guest_id = data.get('guest_id')

            if not all([rating, episode_id, guest_id]):
                return {'errors': ['Missing required fields']}, 400

            episode = Episode.query.get(episode_id)
            guest = Guest.query.get(guest_id)

            if not episode or not guest:
                return {'errors': ['Invalid episode or guest ID']}, 400

            new_appearance = Appearance(
                rating=rating,
                guest_id=guest_id,
                episode_id=episode_id
            )

            db.session.add(new_appearance)
            db.session.commit()

            response = {
                "id": new_appearance.id,
                "rating": new_appearance.rating,
                "guest_id": new_appearance.guest_id,
                "episode_id": new_appearance.episode_id,
                "episode": {
                    "date": episode.date.strftime('%m/%d/%y'),  # Format date as needed
                    "id": episode.id,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }

            return response, 201

        except InterruptedError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400

        except Exception as e:
            return {'errors': [str(e)]}, 500


api.add_resource(EpisodeResource,'/episodes')
api.add_resource(GuestResource,'/guests')
api.add_resource(AppearanceResource,'/appearances')
api.add_resource(EpisodeById,'/episodes/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)