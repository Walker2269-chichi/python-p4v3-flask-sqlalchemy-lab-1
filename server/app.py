# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


#  Earthquake Route (Fetch by ID)
@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = db.session.get(Earthquake, id)  # Avoids SQLAlchemy 2.0 deprecation warning

    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

    return jsonify(earthquake.to_dict())


#  Filter Earthquakes by Magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Convert list of objects to list of dictionaries
    earthquakes_list = [eq.to_dict() for eq in earthquakes]

    response_body = {
        "count": len(earthquakes_list),
        "quakes": earthquakes_list
    }
    
    return jsonify(response_body), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
