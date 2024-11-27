import streamlit as st
import pandas as pd
import datetime
import requests
import time

url = "https://nutrition-calculator.p.rapidapi.com/api/bmi"
headers = {
	"x-rapidapi-key": "1aa81cb2edmsh7ed8d84fdfd1811p18a3b7jsnc6b67afdef93",
	"x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
}

def ageCalculator(dob):
    return today.year  - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def renderUserInputTable(dob, sex, feet, inches, weight, activity):        
        st.header("Your Health Results", divider="gray")
        st.subheader("Your Information")
        
        healthTable = pd.DataFrame({
			"Sex": [sex],
			"Age": [str(ageCalculator(dob)) + " Years Old"],
			"Height": [str(feet) + "'" + str(inches) + '"'],
			"Weight": [weight],
			"Activity Level": [activity],
		})
        st.dataframe(healthTable,750, hide_index=True, on_select="ignore")

def bmiStringReturn (bmi):
    if bmi<18.5:
        return "**underweight**"
    elif bmi<25:
        return "**healthy weight**"
    elif bmi<30:
        return "**overweight**"
    else:
        return "**obese**"
        
def renderBMI(feet, inches, weight):
	querystring = {"measurement_units":"std","feet":f"{feet}","inches":f"{inches}","lbs":f"{int(weight)}"}
	bmiRequest = requests.get(url, headers=headers, params=querystring).json()
	bmiValue = '{0:.1f}'.format(float(bmiRequest["bmi"]))
	st.subheader("Your BMI")
	st.caption("BMI categorical ranges provided by The United States Centers for Disease Control and Prevention.")
	st.write(f"Your BMI is **{bmiValue}** which means you fall into the {bmiStringReturn(float(bmiValue))} category.")
	st.image("bmiChart.jpg")

def renderHealthAssessment(sex, age_value, feet, inches, weight, activity_level):
    healthURL = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"
    queryString = {"measurement_units":"std","sex":f"{sex}","age_value":f"{age_value}","age_type":"yrs","feet":f"{feet}","inches":f"{inches}","lbs":f"{int(weight)}", "pregnancy_lactating": "none", "activity_level": f"{activity_level}"}
    healthRequest = requests.get(healthURL, headers=headers, params=queryString).json()

    st.header("Recommended Nutrition Breakdown", divider="gray")
    st.caption("Nutrient recommendations based on the DRIs are meant to be applied to generally healthy people of a specific age and gender set. Individual nutrient requirements may be higher or lower than the DRIs.")
    
    st.subheader("Calories and Macronutrients")
    macroTableJSON = healthRequest["macronutrients_table"]["macronutrients-table"]
    c1, c2 = st.columns(2)
    c1.html(
        f"<p style='font-weight: 600; margin:0'>Daily Caloric Needs</p><p>{healthRequest["BMI_EER"]["Estimated Daily Caloric Needs"]}</p>"
        )
    for i in range(len(macroTableJSON)):
        if(i==0 or i==5 or i==6 or i==9):
            continue

        if i%2==1:
            c1.html(
                f"<p style='font-weight: 600; margin:0'>{macroTableJSON[i][0]}</p><p>{macroTableJSON[i][1]}</p>"
            )
        else:
            c2.html(
                f"<p style='font-weight: 600; margin:0'>{macroTableJSON[i][0]}</p><p>{macroTableJSON[i][1]}</p>"
            )

    st.subheader("Vitamins")
    vitaminTableJSON = healthRequest["vitamins_table"]["vitamins-table"]
    c3, c4 = st.columns(2)
    for i in range(len(macroTableJSON)):
        if(i==0):
            continue
        if i%2==1:
            c3.html(
                f"<p style='font-weight: 600; margin:0'>{vitaminTableJSON[i][0]}</p><p>{vitaminTableJSON[i][1]}</p>"
            )
        else:
            c4.html(
                f"<p style='font-weight: 600; margin:0'>{vitaminTableJSON[i][0]}</p><p>{vitaminTableJSON[i][1]}</p>"
            )

    



today = datetime.datetime.now()

st.title("Health and Fitness Assistant")
st.caption("Input your information and receive personalized health breakdowns, meal plans, and workout routines tailored to you.")


st.header("Enter Your Health Information", divider="gray")
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
    inches = col2.number_input("Inches", 0, 11, label_visibility="collapsed")
    
    st.write("**Weight**")
    weight = st.number_input("Weight", 0.0, 500.0, "min", 0.1, label_visibility="collapsed")
    
    st.write("**Activity Level**")
    activity = st.radio("Activity Level", ("Inactive","Low Active", "Active", "Very Active"), label_visibility="collapsed", horizontal=True)
    
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
        successMessage = st.success("Your information was successfully processed and your results are ready to go!", icon="🥳")
        renderUserInputTable(dob, sex, feet, inches, weight, activity)
        renderBMI(feet, inches, weight)
        renderHealthAssessment(sex.lower(),ageCalculator(dob), feet, inches, weight, activity)

            
        
        
        