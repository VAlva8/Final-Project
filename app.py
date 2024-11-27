#--Import statements--
import streamlit as st
import pandas as pd
import datetime
import requests
#---------------------

# Global Variables
today = datetime.datetime.now()
#

#-----------------API Retreival Information---------------------
# Calculator API Information
calculatorURL = "https://nutrition-calculator.p.rapidapi.com/api"
calculatorHeaders = {
	"x-rapidapi-key": "1aa81cb2edmsh7ed8d84fdfd1811p18a3b7jsnc6b67afdef93",
	"x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
}

# AI Health Generation API

#---------------------------------------------------------------


#--------------Simple return functions meant for increasing readability--------------
# This takes in the date of birth of the user, then calculates their age in years
def ageCalculator(dob):
    return today.year  - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# This takes in the calculated BMI of the user, the returns the health category they belong to
def bmiStringReturn(bmi):
    if bmi<18.5:
        return "**underweight**"
    elif bmi<25:
        return "**healthy weight**"
    elif bmi<30:
        return "**overweight**"
    else:
        return "**obese**"
#------------------------------------------------------------------------------------- 

#-------Render functions meant for rendering page components-------
# This provides a simple table succintly showing the user's inputs
def renderUserInputTable(dob, sex, feet, inches, weight, activity):        
        st.subheader("Your Information")
        
        userInputTable = pd.DataFrame({
			"Sex": [sex],
			"Age": [str(ageCalculator(dob)) + " Years Old"],
			"Height": [str(feet) + "'" + str(inches) + '"'],
			"Weight": [weight],
			"Activity Level": [activity],
		})

        st.dataframe(userInputTable, 750, hide_index=True, on_select="ignore")


# This calls the API to calculate the user's BMI, then displays it along with categorical information        
def renderBMI(feet, inches, weight):
    # API Call Information
    bmiURL = calculatorURL + "/bmi"
    querystring = {"measurement_units":"std","feet":f"{feet}","inches":f"{inches}","lbs":f"{int(weight)}"}
    bmiRequest = requests.get(bmiURL, headers=calculatorHeaders, params=querystring).json()

    # Reformatting BMI to ony have 1 decimal point
    bmiValue = '{0:.1f}'.format(float(bmiRequest["bmi"]))

    # Web components
    st.subheader("Your BMI")
    st.caption("BMI categorical ranges provided by The United States Centers for Disease Control and Prevention.")
    st.write(f"Your BMI is **{bmiValue}** which means you fall into the {bmiStringReturn(float(bmiValue))} category.")
    st.image("bmiChart.jpg")


# This calls the API and calculates the recommended personalized nutrition for the user, the displays it
def renderNutrition(sex, age_value, feet, inches, weight, activity_level):
    # API Call Information
    nutritionURL = calculatorURL + "/nutrition-info"
    queryString = {"measurement_units":"std","sex":f"{sex}","age_value":f"{age_value}","age_type":"yrs","feet":f"{feet}","inches":f"{inches}","lbs":f"{int(weight)}", "pregnancy_lactating": "none", "activity_level": f"{activity_level}"}
    nutritionRequest = requests.get(nutritionURL, headers=calculatorHeaders, params=queryString).json()

    # Web components for this section
    st.header("Recommended Nutrition Breakdown", divider="gray")
    st.caption("Nutrient recommendations based on the DRIs are meant to be applied to generally healthy people of a specific age and gender set. Individual nutrient requirements may be higher or lower than the DRIs.")
    

    # Web components for the Calorie and Macros section
    st.subheader("Calories and Macronutrients")
    macroJSON = nutritionRequest["macronutrients_table"]["macronutrients-table"]
    macroCol1, macroCol2, macroCol3 = st.columns(3)
    macroCol1.html(f"<p style='font-weight: 600; margin:0'>Daily Caloric Needs</p><p>{nutritionRequest["BMI_EER"]["Estimated Daily Caloric Needs"]}</p>")
    colCounter = 1;
    for i in range(len(macroJSON)):
        if(i==0 or i==5 or i==6 or i==9):
            continue

        if colCounter%3==0:
            macroCol1.html(f"<p style='font-weight: 600; margin:0'>{macroJSON[i][0]}</p><p>{macroJSON[i][1]}</p>")
        elif colCounter%3==1:
            macroCol2.html(f"<p style='font-weight: 600; margin:0'>{macroJSON[i][0]}</p><p>{macroJSON[i][1]}</p>")
        else:
            macroCol3.html(f"<p style='font-weight: 600; margin:0'>{macroJSON[i][0]}</p><p>{macroJSON[i][1]}</p>")
        
        colCounter+=1

    # Web components for the Vitamins section
    st.subheader("Vitamins")
    vitaminJSON = nutritionRequest["vitamins_table"]["vitamins-table"]
    vitaminCol1, vitaminCol2, vitaminCol3 = st.columns(3)
    for i in range(len(vitaminJSON)-1):
        if(i==0):
            continue

        if i%3==1:
            vitaminCol1.html(f"<p style='font-weight: 600; margin:0'>{vitaminJSON[i][0]}</p><p>{vitaminJSON[i][1]}</p>")
        elif i%3==2:
            vitaminCol2.html(f"<p style='font-weight: 600; margin:0'>{vitaminJSON[i][0]}</p><p>{vitaminJSON[i][1]}</p>")
        else:
            vitaminCol3.html(f"<p style='font-weight: 600; margin:0'>{vitaminJSON[i][0]}</p><p>{vitaminJSON[i][1]}</p>")
#-----------------------------------------------------------------------


#----------------------------------------------------Main Webpage Code----------------------------------------------------
# Title and caption introducing the user to the website
st.title("Health and Fitness Assistant")
st.caption("Input your information and receive personalized health breakdowns, meal plans, and workout routines tailored to you.")

# Form for user to input all their health information
st.header("Enter Your Health Information", divider="gray")
with st.form("Information Form"):
    # Sex selectbox
    st.write("**Sex**")
    sex = st.selectbox('Sex', ("","Male", "Female"), label_visibility="collapsed")
    
    # Date of birth date input
    st.write("**Date of Birth**")
    dob = st.date_input("Date of Birth", None, datetime.date(1904,1,1), datetime.date(2024, today.month-1, today.day-1), format="MM/DD/YYYY", label_visibility="collapsed")
    
    # Height section with bothe feet and inches
    st.write("**Height**")
    col1, col2 = st.columns(2)
    
    # Feet number input
    col1.write("Feet")
    feet = col1.number_input("Feet", 0, 8, label_visibility="collapsed")
    
    # Inches number input
    col2.write("Inches")
    inches = col2.number_input("Inches", 0, 11, label_visibility="collapsed")
    
    # Weight number input
    st.write("**Weight**")
    weight = st.number_input("Weight", 0.0, 500.0, "min", 0.1, label_visibility="collapsed")
    
    # Activity level radio buttons
    st.write("**Activity Level**")
    activity = st.radio("Activity Level", ("Inactive","Low Active", "Active", "Very Active"), label_visibility="collapsed", horizontal=True)
    
    # Submit buttons for health form
    healthInfoSubmit = st.form_submit_button()

# This check if the form was submitted    
if healthInfoSubmit:

    # Boolean meant to check if there was a wrong input from the user
    error = False

    # If there was an error, the is statments turn the boolean true
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
    
    # The rest of the code runs iff there is no errored input
    if not error:
        successMessage = st.success("Your information was successfully processed!", icon="🥳")
        st.header("Your Health Results", divider="gray")
        renderUserInputTable(dob, sex, feet, inches, weight, activity)
        renderBMI(feet, inches, weight)
        renderNutrition(sex.lower(),ageCalculator(dob), feet, inches, weight, activity)