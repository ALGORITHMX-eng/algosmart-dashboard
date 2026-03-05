def farm_finance(farm_size, crop, soil_moisture):

    yield_data = {
        "Rice": 5,
        "Maize": 2.5,
        "Tomatoes": 25
    }

    price = {
        "Rice": 420000,
        "Maize": 300000,
        "Tomatoes": 250000
    }

    base_yield = yield_data[crop]

    # Soil health adjustment
    if soil_moisture < 25:
        adjustment = 0.75
    elif soil_moisture < 40:
        adjustment = 0.9
    else:
        adjustment = 1

    expected_yield = farm_size * base_yield * adjustment

    market_value = expected_yield * price[crop]

    # Loan estimation
    loan_required = farm_size * 180000

    if expected_yield > farm_size * base_yield * 0.9:
        risk = "A (Low)"
    elif expected_yield > farm_size * base_yield * 0.75:
        risk = "B (Medium)"
    else:
        risk = "C (High)"

    return expected_yield, market_value, loan_required, risk


