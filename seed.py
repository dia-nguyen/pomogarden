"""Seed database with sample data from CSV Files."""
from app import db
from models import Seed

db.drop_all()
db.create_all()

seeds = [
    {
        "name": "corn",
        "seed_sprite" : "corn-seed.png",
        "sprout_sprite" : "corn-sprout.png",
        "seedling_sprite" : "corn-seedling.png",
        "budding_sprite" : "corn-budding.png",
        "ripe_sprite" : "corn-ripe.png",
        "plant_sprite" : "corn-plant.png",
        "buy_price": 25,
        "sell_price": 100
    },
    {
        "name": "tomato",
        "seed_sprite" : "tomato-seed.png",
        "sprout_sprite" : "tomato-sprout.png",
        "seedling_sprite" : "tomato-seedling.png",
        "budding_sprite" : "tomato-budding.png",
        "ripe_sprite" : "tomato-ripe.png",
        "plant_sprite" : "tomato-plant.png",
        "buy_price": 25,
        "sell_price": 100
    },
    {
        "name": "carrot",
        "seed_sprite" : "carrot-seed.png",
        "sprout_sprite" : "carrot-sprout.png",
        "seedling_sprite" : "carrot-seedling.png",
        "budding_sprite" : "carrot-budding.png",
        "ripe_sprite" : "carrot-ripe.png",
        "plant_sprite" : "carrot-plant.png",
        "buy_price": 25,
        "sell_price": 100
    },
]

for seed in seeds:
    new_seed = Seed(
        name=seed["name"],
        seed_sprite=seed["seed_sprite"],
        sprout_sprite=seed["sprout_sprite"],
        seedling_sprite=seed["seedling_sprite"],
        budding_sprite=seed["budding_sprite"],
        ripe_sprite=seed["ripe_sprite"],
        plant_sprite=seed["plant_sprite"],
        buy_price=seed["buy_price"],
        sell_price=seed["sell_price"]
    )
    db.session.add(new_seed)
    db.session.commit()