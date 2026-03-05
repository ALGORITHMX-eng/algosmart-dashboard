def calculate_carbon(farm_size, crop):

    coefficients = {
        "Rice": 1.2,
        "Maize": 0.8,
        "Tomatoes": 0.6
    }

    return farm_size * coefficients[crop]