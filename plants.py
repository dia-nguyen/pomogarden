from models import Seed, PlantPlot, User

def plant_shop():
    """Renders shop with seeds"""

    seeds = Seed.query.all()

    return seeds