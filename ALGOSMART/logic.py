def irrigation_decision(soil_moisture, humidity, rain, crop):

    water_need = {
        "Rice": 60,
        "Maize": 45,
        "Tomatoes": 40
    }

    threshold = water_need[crop]

    if soil_moisture < threshold and rain == 0 and humidity < 80:
        decision = "IRRIGATE"
        reason = f"Soil: {soil_moisture}% | Forecast: {rain}mm | Crop: {crop} | Decision: Critical Need"

    else:
        decision = "DON'T IRRIGATE"
        reason = f"Soil: {soil_moisture}% | Humidity: {humidity}% | Rain expected"

    return decision, reason

def calculate_water_needed(crop, soil_moisture, farm_size):

    crop_water_need = {
        "Rice": 12000,
        "Maize": 7000,
        "Cassava": 6500,
        "Tomatoes": 6000
    }

    optimal_moisture = {
        "Rice": 60,
        "Maize": 40,
        "Cassava": 38,
        "Tomatoes": 45
    }

    target = optimal_moisture.get(crop, 40)

    deficit = max(0, target - soil_moisture)

    water = deficit * crop_water_need.get(crop, 7000) * farm_size / 10

    return int(water)