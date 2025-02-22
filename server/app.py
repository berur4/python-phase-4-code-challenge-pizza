#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = False  # Suppress Flask-RESTful warning
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code Challenge</h1>"

class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([r.to_dict() for r in restaurants])

class RestaurantResource(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)  # Use db.session.get instead of Query.get
        if restaurant:
            return jsonify(restaurant.to_dict(rules=("-restaurant_pizzas.restaurant",)))
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)  # Use db.session.get instead of Query.get
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return "", 204
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([p.to_dict() for p in pizzas])

class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(), 201  # FIXED response formatting
        except ValueError:
            return {"errors": ["validation errors"]}, 400  # FIXED error response


api.add_resource(RestaurantListResource, "/restaurants")
api.add_resource(RestaurantResource, "/restaurants/<int:id>")
api.add_resource(PizzaListResource, "/pizzas")
api.add_resource(RestaurantPizzaResource, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)