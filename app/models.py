from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates
from datetime import datetime
import pytz
from marshmallow import Schema, fields

tz = pytz.timezone('Africa/Nairobi')

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    super_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now(tz))
    updated_at = db.Column(db.DateTime, default=datetime.now(tz), onupdate=datetime.now(tz))
    powers = relationship('HeroPower', back_populates='hero')

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz))
    updated_at = db.Column(db.DateTime, default=datetime.now(tz), onupdate=datetime.now(tz))
    heroes = relationship('HeroPower', back_populates='power')

    @validates('description')
    def validate_description(self, key, description):
        assert len(description) >= 20, "Description should be at least 20 characters long"
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Enum('Strong', 'Weak', 'Average'), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(tz))
    updated_at = db.Column(db.DateTime, default=datetime.now(tz), onupdate=datetime.now(tz))
    hero = relationship('Hero', back_populates='powers')
    power = relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], "Strength should only be one of the following: 'Strong', 'Weak', 'Average'"
        return strength

class HeroSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    super_name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    powers = fields.Nested('HeroPowerSchema', many=True)

    class Meta:
        model = Hero


class PowerSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    heroes = fields.Nested(HeroSchema, many=True)

    class Meta:
        model = Power

class HeroPowerSchema(Schema):
    id = fields.Int()
    strength = fields.Str()
    hero_id = fields.Int()
    power_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        model = HeroPower