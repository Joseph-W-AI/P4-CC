from flask import Flask, jsonify, request
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate
from models import HeroSchema, PowerSchema


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True) 
power_schema = PowerSchema() 
powers_schema = PowerSchema(many=True)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    result = heroes_schema.dump(heroes)
    return jsonify(result)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    result = hero_schema.dump(hero)
    return jsonify(result)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    result = powers_schema.dump(powers)
    return jsonify(result)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    return power_schema.jsonify(power)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    description = request.json.get('description')
    if description is None or len(description) < 20:
        return jsonify({'errors': ['validation errors']}), 400
    power.description = description
    db.session.commit()
    return power_schema.jsonify(power)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    strength = request.json.get('strength')
    power_id = request.json.get('power_id')
    hero_id = request.json.get('hero_id')
    if strength not in ['Strong', 'Weak', 'Average'] or power_id is None or hero_id is None:
        return jsonify({'errors': ['validation errors']}), 400
    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)
    if power is None or hero is None:
        return jsonify({'errors': ['validation errors']}), 400
    hero_power = HeroPower(strength=strength, power=power, hero=hero)
    db.session.add(hero_power)
    db.session.commit()
    return hero_schema.jsonify(hero)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
