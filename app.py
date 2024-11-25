import streamlit as st
import http.client

conn = http.client.HTTPSConnection("nutrition-calculator.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "1aa81cb2edmsh7ed8d84fdfd1811p18a3b7jsnc6b67afdef93",
    'x-rapidapi-host': "nutrition-calculator.p.rapidapi.com"
}
conn.request("GET", "/api/bmi?measurement_units=std&feet=5&inches=2&lbs=120", headers=headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

st.title("Health and Nutrition Tracker")
st.caption("Here we describe what the website does or just a general sales pitch for new people coming on to the site")