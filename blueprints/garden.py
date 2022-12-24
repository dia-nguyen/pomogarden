from flask import Blueprint, redirect, url_for, render_template, flash, g
from flask_login import login_required, current_user
from plants import plant_shop
from models import db, Seed, PlantPlot

garden = Blueprint('garden', __name__)

@garden.post('/buy/<seed>')
@login_required
def buy_seed(seed):
    """Buy seed from shop and to user"""
    if len(current_user.available_plots) < 3 :
        seedInfo = Seed.query.get(seed)
        current_user.buy_seed(seedInfo)
        db.session.commit()

        flash(f"You bought {seed} seeds!")
    else:
        flash(f"Your inventory is full!")

    return redirect(url_for('main.index'))


@garden.post("/<plant_plot_id>/sow")
@login_required
def sow_plot(plant_plot_id):
    """Sow plot"""
    plant_plot = PlantPlot.query.get(plant_plot_id)

    if plant_plot.status == "empty":
        plant_plot.sow_plot()
        db.session.commit()
        return redirect(url_for("main.index"))


@garden.post("/<plant_plot_id>/plant")
@login_required
def plant_plot(plant_plot_id):
    """Plant in plot"""
    plant_plot = PlantPlot.query.get(plant_plot_id)
    seed = Seed.query.get(plant_plot.name)

    if plant_plot.status == "sowed":
        plant_plot.plant_seed(seed)
        db.session.commit()
        return redirect(url_for("main.index"))


@garden.post("/<plant_plot_id>/water")
@login_required
def water_plot(plant_plot_id):
    """Plant in plot"""
    plant_plot = PlantPlot.query.get(plant_plot_id)

    if plant_plot.status == "planted" and plant_plot.watered == False or plant_plot.status == "thirsty":
        plant_plot.water_plant()
        db.session.commit()
        return redirect(url_for("main.index"))


@garden.post("/<plant_plot_id>/sell")
@login_required
def harvest_and_sell(plant_plot_id):
    """Harvest and sell plant in plot"""
    plant_plot = PlantPlot.query.get(plant_plot_id)
    seed = Seed.query.get(plant_plot.name)

    if plant_plot.age == "ripe":
        plant_plot.harvest_and_sell_plant(seed)
        flash(f"You sold your {plant_plot.name} for {seed.sell_price} coins!")
        db.session.commit()
        return redirect(url_for("main.index"))


@garden.post("/next-day")
@login_required
def next_day():
    """Go to next day"""
    plant_plots = current_user.plant_plots

    for plot in plant_plots:
        if plot.watered:
            seed = Seed.query.get(plot.name)
            plot.age_one_day(seed)

    db.session.commit()

    return redirect(url_for("main.index"))
