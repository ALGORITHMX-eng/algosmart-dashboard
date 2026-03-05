import streamlit as st
import pandas as pd
import random
import requests
from logic import calculate_water_needed

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="AlgoSmart Agriculture",
    layout="wide",
    page_icon="🌱"
)

# ===================================
# CUSTOM STYLE
# ===================================

st.markdown("""
<style>

.main {
    background-color:#0f172a;
}

h1,h2,h3,h4 {
    color:white;
}

.stMetric {
    background-color:#1e293b;
    padding:15px;
    border-radius:12px;
}

.css-1d391kg {
    background-color:#020617;
}

</style>
""", unsafe_allow_html=True)


# ===================================
# WEATHER API
# ===================================

API_KEY = "62acfe029ef72824cce2ced7d280874e"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},NG&appid={API_KEY}&units=metric"

    try:
        r = requests.get(url).json()

        temp = r["main"]["temp"]
        humidity = r["main"]["humidity"]
        rain = r.get("rain", {}).get("1h", 0)

        return temp, humidity, rain

    except:
        return 30,70,0


# ===================================
# CARBON CALC
# ===================================

def carbon_calc(farm_size,crop):

    coeff = {
        "Rice":0.9,
        "Maize":0.8,
        "Tomatoes":0.7
    }

    return farm_size * coeff[crop]


# ===================================
# FINANCE ENGINE
# ===================================

def finance_engine(farm_size,crop,soil):

    yield_map = {
        "Rice":5,
        "Maize":2.5,
        "Tomatoes":25
    }

    price_map = {
        "Rice":420000,
        "Maize":300000,
        "Tomatoes":250000
    }

    base = yield_map[crop]

    if soil < 25:
        adjust = 0.7
    elif soil < 40:
        adjust = 0.9
    else:
        adjust = 1

    expected_yield = farm_size * base * adjust
    value = expected_yield * price_map[crop]

    loan = farm_size * 180000

    if adjust >= 0.9:
        risk = "A (Low)"
    elif adjust >= 0.75:
        risk = "B (Moderate)"
    else:
        risk = "C (High)"

    return expected_yield,value,loan,risk


# ===================================
# IRRIGATION AI
# ===================================

def irrigation_ai(soil,humidity,rain):

    if soil < 35 and humidity < 80 and rain < 1:
        decision = "IRRIGATE"
        water = random.randint(10000,20000)

    else:
        decision = "DO NOT IRRIGATE"
        water = 0

    return decision,water


# ===================================
# SOIL NUTRIENT AI
# ===================================

def fertilizer_ai(nutrient,farm_size):

    if nutrient >= 60:
        return "Soil nutrients adequate",0

    elif nutrient >= 40:
        return "Moderate nutrient deficiency",farm_size*20

    else:
        return "Severe nutrient deficiency",farm_size*40


# ===================================
# PEST AI
# ===================================

def pest_ai(level,farm_size):

    if level < 30:
        return "Low Pest Risk",0

    elif level < 60:
        return "Moderate Pest Risk",farm_size*2

    else:
        return "High Pest Risk",farm_size*4


# ===================================
# SIDEBAR
# ===================================

st.sidebar.title("Farm Configuration")

city = st.sidebar.selectbox(
    "Location",
    [
        "Lagos","Ibadan","Abuja","Kano","Kaduna",
        "Port Harcourt","Enugu","Jos","Benin"
    ]
)

crop = st.sidebar.selectbox(
    "Crop Type",
    ["Rice","Maize","Tomatoes"]
)

farm_size = st.sidebar.slider(
    "Farm Size (Hectares)",
    1,50,5
)

soil = st.sidebar.slider(
    "Soil Moisture %",
    0,100,30
)

soil_nutrient = st.sidebar.slider(
    "Soil Nutrient %",
    0,100,55
)

pest_level = st.sidebar.slider(
    "Pest Activity Level",
    0,100,30
)

# ===================================
# CALCULATIONS
# ===================================

temp,humidity,rain = get_weather(city)

carbon = carbon_calc(farm_size,crop)

yield_tonnes,value,loan,risk = finance_engine(
    farm_size,crop,soil
)

decision,water = irrigation_ai(
    soil,humidity,rain
)

nutrient_status,fertilizer = fertilizer_ai(
    soil_nutrient,farm_size
)

pest_status,pesticide = pest_ai(
    pest_level,farm_size
)

water_needed = calculate_water_needed(
    crop,
    soil,
    farm_size
)


# ===================================
# TITLE
# ===================================

st.title("🌱 AlgoSmart Climate Smart Agriculture Dashboard")

st.write(
"AI-powered decision support for irrigation, finance, crop health and climate risk."
)

st.divider()


# ===================================
# WEATHER METRICS
# ===================================

c1,c2,c3,c4 = st.columns(4)

c1.metric("Temperature",f"{temp:.1f} °C")
c2.metric("Humidity",f"{humidity}%")
c3.metric("Rain Forecast",f"{rain} mm")
c4.metric("Carbon Captured",f"{carbon:.2f} Tonnes")


# ===================================
# WATER AI
# ===================================

st.subheader("💧 AI Water Requirement")

st.metric(
    "Water Needed Today",
    f"{water_needed:,} Litres"
)


# ===================================
# FINANCE TABLE
# ===================================

st.subheader("💰 Farm Financial Projection")

df = pd.DataFrame({

"Metric":[
"Expected Yield",
"Market Value",
"Loan Requirement",
"Risk Score"
],

"Value":[
f"{yield_tonnes:.1f} tonnes",
f"₦{value:,.0f}",
f"₦{loan:,.0f}",
risk
]

})

st.dataframe(df,use_container_width=True)


# ===================================
# SOIL TREND
# ===================================

st.subheader("📈 7-Day Soil Moisture Trend")

trend = [soil + random.randint(-5,5) for _ in range(7)]

trend_df = pd.DataFrame({
"Soil Moisture":trend
})

st.line_chart(trend_df)


# ===================================
# IRRIGATION AI
# ===================================

st.subheader("🚿 Irrigation AI Recommendation")

if decision == "IRRIGATE":
    st.success(f"Irrigate Now – {water:,} Litres Recommended")
else:
    st.warning("No Irrigation Needed")


with st.expander("AI Explanation"):

    st.write(f"""
Soil Moisture: {soil} %

Humidity: {humidity} %

Rain Forecast: {rain} mm

Crop: {crop}

Decision: {decision}
""")


# ===================================
# SOIL HEALTH
# ===================================

st.subheader("🌾 Soil Health Intelligence")

c1,c2 = st.columns(2)

c1.metric("Soil Nutrient Level",f"{soil_nutrient}%")

if fertilizer == 0:
    c2.success("No Fertilizer Needed")

else:
    c2.warning(f"Apply {fertilizer} kg Fertilizer")

st.info(nutrient_status)


# ===================================
# PEST MONITORING
# ===================================

st.subheader("🐛 Pest Monitoring")

if pesticide == 0:
    st.success(pest_status)

else:
    st.warning(
        f"{pest_status} — Apply {pesticide} Litres pesticide"
)