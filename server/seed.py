#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Delete data in the correct order to avoid foreign key constraint issues
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Create restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="address1")
    bistro = Restaurant(name="Sanjay's Pizza", address="address2")
    palace = Restaurant(name="Kiki's Pizza", address="address3")
    restaurants = [shack, bistro, palace]

    # Create pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    # Add restaurants and pizzas to the session first
    db.session.add_all(restaurants + pizzas)
    db.session.commit()

    # Create RestaurantPizza associations
    print("Creating RestaurantPizza...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=20)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=15)

    # Add RestaurantPizza to the session and commit
    db.session.add_all([pr1, pr2, pr3])
    db.session.commit()

    print("Seeding done!")