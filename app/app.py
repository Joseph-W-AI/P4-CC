from flask import Flask, jsonify, request
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.serialize for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.serialize)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.serialize for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.serialize)

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
    return jsonify(power.serialize)

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
    return jsonify(hero.serialize)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
