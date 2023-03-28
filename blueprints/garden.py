from flask import Blueprint, jsonify
from flask_login import current_user
from models import db, Seed, PlantPlot, User

garden = Blueprint('garden', __name__)

def user_plants_list(user_id):
    """Returns serialized list of plant plots that have not been sold"""
    user_plants = User.query.get(user_id).plant_plots
    return [plant.serialize() for plant in user_plants if plant.status != "sold"]

@garden.get('/plants')
def get_user_plants():
    """Returns JSON with user id and available plants and plots"""
    if current_user.is_authenticated:
        plants_list = user_plants_list(current_user.id)
        return jsonify(plants = plants_list)
    return (jsonify(status="error", message="You are not logged in"))

@garden.get('/coins')
def get_user_coins():
    """Returns JSON with user id and available plants and plots"""
    if current_user.is_authenticated:
        coins = current_user.coins
        return jsonify(coins=coins)
    return (jsonify(status="error", message="You are not logged in"))



@garden.post('/plants/<seed>/buy')
def buy_seed(seed):
    """Buy seed from shop and to user"""
    if current_user.is_authenticated:
        if len(current_user.available_plots) < 3 :
            new_seed = Seed.query.get_or_404(seed)
            current_user.buy_seed(new_seed)
            db.session.commit()
            return (jsonify(plant=new_seed.serialize(),status="success", message=f"Successfully bought {new_seed.name} seeds") , 201)

        return (jsonify(status="error", message="Your inventory is full"))



@garden.patch("/plants/<plant_id>/sow")
def sow_plot(plant_id):
    """Sow plot"""
    if current_user.is_authenticated:
        plant_plot = PlantPlot.query.get_or_404(plant_id)
        if plant_plot.status == "empty":
            plant_plot.sow_plot()
            db.session.commit()

            return jsonify(status="success", plant=plant_plot.serialize())
        return (jsonify(status="error", message="This plot cannot be sowed"))



@garden.patch("/plants/<plant_id>/plant")
def plant_plot(plant_id):
    """Plant in plot"""
    if current_user.is_authenticated:
        plant_plot = PlantPlot.query.get_or_404(plant_id)
        seed = Seed.query.get_or_404(plant_plot.name)

        if plant_plot.status == "sowed":
            plant_plot.plant_seed(seed)
            db.session.commit()

            return jsonify(status="success", plant=plant_plot.serialize())
        return (jsonify(status="error", message="Cannot plant seed"))


@garden.patch("/plants/<plant_id>/water")
def water_plot(plant_id):
    """Plant in plot"""
    if current_user.is_authenticated:
        plant_plot = PlantPlot.query.get(plant_id)

        if plant_plot.status == "planted" and plant_plot.watered == False or plant_plot.status == "thirsty" or plant_plot.age != "ripe":
            plant_plot.water_plant()
            db.session.commit()
            return jsonify(status="success", plant=plant_plot.serialize())
        return (jsonify(status="error", message="Cannot be watered"))


@garden.patch("/plants/<plant_plot>/sell")
def harvest_and_sell(plant_plot):
    """Harvest and sell plant in plot"""
    if current_user.is_authenticated:
        plant_plot = PlantPlot.query.get(plant_plot)
        seed = Seed.query.get(plant_plot.name)

        if plant_plot.age == "ripe" and plant_plot.status != "sold":
            plant_plot.harvest_and_sell_plant(seed)

            db.session.commit()
            return jsonify(status="success", message=f"You sold your {plant_plot.name} for {seed.sell_price} coins!", price= seed.sell_price, plant=plant_plot.serialize())

        return (jsonify(status="error", message="Cannot be sold"))



@garden.post("/plants/age")
def next_day():
    """Go to next day"""
    if current_user.is_authenticated:
        plant_plots = current_user.plant_plots

        for plot in plant_plots:
            if plot.watered:
                seed = Seed.query.get(plot.name)
                plot.age_one_day(seed)

        db.session.commit()
        plants_list = user_plants_list(current_user.id)

        return jsonify(status="success", plants=plants_list)
