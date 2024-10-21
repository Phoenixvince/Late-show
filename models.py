from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, ValidationError

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    # Serialize rules to prevent deep recursion
    serialize_rules = ('-appearances.episode', '-appearances.guest.appearances')

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # Relationship to Appearance
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete')

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-appearances.guest', '-appearances.episode.appearances')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    occupation = db.Column(db.String(90), nullable=False)

    # Relationship to Appearance
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete')

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    # Relationships
    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    # Validation
    def __init__(self, rating, guest_id, episode_id):
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        self.rating = rating
        self.guest_id = guest_id
        self.episode_id = episode_id
