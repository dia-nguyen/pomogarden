from flask import Blueprint, jsonify, g
from flask_login import current_user
from models import db, Seed, PlantPlot, User
from flask_jwt_extended import (
    jwt_required,
)
garden = Blueprint('garden', __name__)

def user_plants_list(user_id):
    """Returns serialized list of plant plots that have not been sold"""
    user_plants = User.query.get(user_id).plant_plots
    user_plants = sorted(user_plants, key=lambda plant: (plant.location is None, plant.location))
    return [plant.serialize() for plant in user_plants if plant.status != "sold"]

@garden.get('/plants')
@jwt_required()
def get_user_plants():
    """Returns JSON with user id and available plants and plots"""
    plants_list = user_plants_list(g.user.id)
    return jsonify(plants = plants_list)

@garden.get('/coins')
@jwt_required()
def get_user_coins():
    """Returns JSON with user id and available plants and plots"""
    coins = current_user.coins
    return jsonify(coins=coins)



@garden.post('/plants/<seed>/buy')
@jwt_required()
def buy_seed(seed):
    """Buy seed from shop and to user"""

    if len([plot for plot in g.user.plant_plots if plot.status == "empty"]) < 3:
        new_seed = Seed.query.get_or_404(seed)
        g.user.buy_seed(new_seed)
        db.session.commit()
        plants_list = user_plants_list(g.user.id)
        return jsonify(plants = plants_list)

        # return (jsonify(plant=new_seed.serialize(),status="success", message=f"Successfully bought {new_seed.name} seeds") , 201)

    return (jsonify(status="error", message="Your inventory is full")), 400



@garden.patch("/plants/<plant_id>/sow")
@jwt_required()
def sow_plot(plant_id):
    """Sow plot"""
    plant_plot = PlantPlot.query.get_or_404(plant_id)
    if plant_plot.status == "empty":
        plant_plot.sow_plot()
        db.session.commit()

        plants_list = user_plants_list(g.user.id)
        return jsonify(plants = plants_list)



@garden.patch("/plants/<plant_id>/plant")
@jwt_required()
def plant_plot(plant_id):
    """Plant in plot"""
    plant_plot = PlantPlot.query.get_or_404(plant_id)
    seed = Seed.query.get_or_404(plant_plot.name)

    if plant_plot.status == "sowed":
        plant_plot.plant_seed(seed)
        db.session.commit()

        plants_list = user_plants_list(g.user.id)
        return jsonify(plants = plants_list)


@garden.patch("/plants/<plant_id>/water")
@jwt_required()
def water_plot(plant_id):
    """Plant in plot"""
    plant_plot = PlantPlot.query.get(plant_id)

    if plant_plot.status == "planted" and plant_plot.watered == False or plant_plot.status == "thirsty" or plant_plot.age != "ripe":
        plant_plot.water_plant()
        db.session.commit()
        plants_list = user_plants_list(g.user.id)
        return jsonify(plants = plants_list)


@garden.patch("/plants/<plant_plot>/sell")
@jwt_required()
def harvest_and_sell(plant_plot):
    """Harvest and sell plant in plot"""
    plant_plot = PlantPlot.query.get(plant_plot)
    seed = Seed.query.get(plant_plot.name)

    if plant_plot.age == "ripe" and plant_plot.status != "sold":
        plant_plot.harvest_and_sell_plant(seed)

        db.session.commit()

        plants_list = user_plants_list(g.user.id)
        return jsonify(status="success",plants = plants_list, message=f"You sold your {plant_plot.name} for {seed.sell_price} coins!", price= seed.sell_price, plant=plant_plot.serialize())




@garden.post("/plants/age")
@jwt_required()
def next_day():
    """Go to next day"""
    plant_plots = g.user.plant_plots

    for plot in plant_plots:
        if plot.watered:
            seed = Seed.query.get(plot.name)
            plot.age_one_day(seed)

    db.session.commit()
    plants_list = user_plants_list(g.user.id)

    return jsonify(status="success", plants=plants_list)
