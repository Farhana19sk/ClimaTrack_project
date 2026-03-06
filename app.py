import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import base64
import os

# ================= CONFIG =================
API_KEY = st.secrets["OPENWEATHER_API_KEY"]  # Replace with your OpenWeather API key
st.set_page_config(page_title="ClimaTrack", layout="wide")

# ================= SAFE BACKGROUND FUNCTION =================
def set_background():
    image_path = os.path.join("assets", "background.jpeg")

    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .title-text {{
            font-size: 40px;
            font-weight: bold;
            color: white;
        }}
        </style>
        """
        st.markdown(bg_style, unsafe_allow_html=True)
    else:
        st.warning("Background image not found in assets folder.")

set_background()

# ================= HEADER WITH LOGO =================
col1, col2 = st.columns([1, 6])

with col1:
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.warning("Logo not found in assets folder.")

with col2:
    st.markdown('<div class="title-text">ClimaTrack - Climate Intelligence Platform</div>', unsafe_allow_html=True)

st.markdown("---")

# ================= NAVIGATION =================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "🌍 Global Map",
    "📊 Forecast",
    "🗺 Compare Cities",
    "📈 Climate Trends",
    "🚨 Alerts"
])

# ================= HOME TAB =================
with tab1:
    st.header("Real-Time Weather")

    city = st.text_input("Enter City Name")
    unit = st.radio("Select Unit", ["Celsius (°C)", "Fahrenheit (°F)"])

    if st.button("Get Weather"):
        if city:
            units = "metric" if "Celsius" in unit else "imperial"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Temperature", f"{data['main']['temp']}°")
                    st.metric("Humidity", f"{data['main']['humidity']}%")

                with col2:
                    st.metric("Feels Like", f"{data['main']['feels_like']}°")
                    st.metric("Wind Speed", f"{data['wind']['speed']} m/s")

                with col3:
                    sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
                    sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
                    st.write("🌅 Sunrise:", sunrise.strftime("%H:%M:%S"))
                    st.write("🌇 Sunset:", sunset.strftime("%H:%M:%S"))

                st.success(f"Condition: {data['weather'][0]['description'].title()}")

            else:
                st.error("City not found. Please enter a valid city name.")
        else:
            st.warning("Please enter a city name.")

# ================= GLOBAL MAP =================
with tab2:
    st.header("🌍 Global Weather Map")
    st.map()

# ================= FORECAST =================
with tab3:
    st.header("📊 5-Day Forecast (Coming Soon)")
    st.info("You can integrate OpenWeather Forecast API here.")

# ================= COMPARE CITIES =================
with tab4:
    st.header("🗺 Compare Cities")

    city1 = st.text_input("Enter First City")
    city2 = st.text_input("Enter Second City")

    if st.button("Compare Weather"):
        if city1 and city2:
            url1 = f"http://api.openweathermap.org/data/2.5/weather?q={city1}&appid={API_KEY}&units=metric"
            url2 = f"http://api.openweathermap.org/data/2.5/weather?q={city2}&appid={API_KEY}&units=metric"

            data1 = requests.get(url1).json()
            data2 = requests.get(url2).json()

            if data1.get("cod") == 200 and data2.get("cod") == 200:
                st.subheader("Temperature Comparison (°C)")
                st.write(f"{city1}: {data1['main']['temp']}°C")
                st.write(f"{city2}: {data2['main']['temp']}°C")
            else:
                st.error("One or both cities not found.")
        else:
            st.warning("Please enter both city names.")

# ================= CLIMATE TRENDS =================
with tab5:
    st.header("📈 Climate Trends (Sample Data)")

    days = [1, 2, 3, 4, 5]
    temps = [20, 22, 19, 23, 25]

    plt.figure()
    plt.plot(days, temps)
    plt.xlabel("Days")
    plt.ylabel("Temperature (°C)")
    st.pyplot(plt)

# ================= ALERTS =================
with tab6:
    st.header("🚨 Weather Alerts")
    st.warning("No active extreme weather alerts currently.")
