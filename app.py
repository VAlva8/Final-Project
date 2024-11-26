import streamlit as st
import pandas as pd
import datetime
import requests

def renderUserInputTable(dob, sex, feet, inches, weight, activity):
        age = today.year  - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        st.header("Your Health Results")
        st.subheader("Your Information")
        
        healthTable = pd.DataFrame({
			"Sex": [sex],
			"Age": [str(age) + " Years Old"],
			"Height": [str(feet) + "'" + str(inches) + '"'],
			"Weight": [weight],
			"Activity Level": [activity],
		})
        st.dataframe(healthTable,750, hide_index=True, on_select="ignore")

url = "https://nutrition-calculator.p.rapidapi.com/api/bmi"
querystring = {"measurement_units":"std","feet":"5","inches":"2","lbs":"120"}
headers = {
	"x-rapidapi-key": "1aa81cb2edmsh7ed8d84fdfd1811p18a3b7jsnc6b67afdef93",
	"x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring).json()
st.write(response["bmi"])

today = datetime.datetime.now()

st.title("Health and Nutrition Tracker")
st.caption("Here we describe what the website does or just a general sales pitch for new people coming on to the site")


st.header("Enter Your Health Information.")
with st.form("Information Form"):
    st.write("**Sex**")
    sex = st.selectbox('Sex', ("","Male", "Female"), label_visibility="collapsed")
    
    st.write("**Date of Birth**")
    dob = st.date_input("Date of Birth", None, datetime.date(1904,1,1), datetime.date(2024, today.month-1, today.day-1), format="MM/DD/YYYY", label_visibility="collapsed")
    
    st.write("**Height**")
    col1, col2 = st.columns(2)
    
    col1.write("Feet")
    feet = col1.number_input("Feet", 0, 8, label_visibility="collapsed")
    
    col2.write("Inches")
    inches = col2.number_input("Inches", 0, 12, label_visibility="collapsed")
    
    st.write("**Weight**")
    weight = st.number_input("Weight", 0.0, 500.0, "min", 0.1, label_visibility="collapsed")
    
    st.write("**Activity Level**")
    activity = st.radio("Activity Level", ("Inactive","Low Activity", "Active", "Very Active"), label_visibility="collapsed")
    
    healthInfoSubmit = st.form_submit_button()
    
if healthInfoSubmit:
    error = False
    if sex == "":
        error = True
        st.error("Please input your sex.", icon="🚨")
    if dob == None:
        error = True
        st.error("Please enter your date of birth.", icon="🚨")
    if feet == 0 and inches == 0:
        error = True
        st.error("Please enter your height.", icon="🚨")
    if weight == 0.00:
        error = True
        st.error("Please enter your weight.", icon="🚨")
        
    if not error:
        st.success("Your information was successfully processed and your results are ready to go!", icon="🥳")
        renderUserInputTable(dob, sex, feet, inches, weight, activity)
            
        
        
        