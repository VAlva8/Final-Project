#--Import statements--
import streamlit as st
import pandas as pd
import datetime
import requests
import time
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

# Nutrionix API
nutriID = "90f57e55"
nutriKey = "6c7ba2a09a41a20ec6ffe2654058da60"
nutriURL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
nutriHeaders = {
    'Content-Type': 'application/json',
    'x-app-id': nutriID,
    'x-app-key': nutriKey,
}

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
    
    weightLossBox = st.checkbox("Are you looking to lose weight?")

    # Web components for the Calorie and Macros section
    st.subheader("Calories and Macronutrients")
    macroJSON = nutritionRequest["macronutrients_table"]["macronutrients-table"]
    macroCol1, macroCol2, macroCol3 = st.columns(3)
    calories = nutritionRequest["BMI_EER"]["Estimated Daily Caloric Needs"]
    calories = calories[:len(calories)-9]
    calories = calories.replace(",", "")
    if weightLossBox:
        macroCol1.html(f"<p style='font-weight: 600; margin:0'>Daily Caloric Needs</p><p>{int(calories)-500} kcal/day</p>")
    else:
        macroCol1.html(f"<p style='font-weight: 600; margin:0'>Daily Caloric Needs</p><p>{calories} kcal/day</p>")

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

def renderFoodIntake():
    st.header("Food Intake Analysis", divider="gray")
    st.subheader("Food Nutrition Checker")
    try:
        userInput = st.text_input("Type the food you wish to see the nutrient breakdown of. For example, search 'Pizza' or 'Salad'.")
        if userInput:
            parameters = {'query': f"{userInput}",}
            response = requests.post(url=nutriURL, json=parameters, headers=nutriHeaders).json()
            result = response["foods"][0]
            foundMessage = st.success("Food found successfully!", icon="✅")
            st.html(f"<h4>{result["food_name"].title()}</h4><hr style='margin:0'>")
            fi1, fi2, fi3 = st.columns(3)
            columnCounter = 0
            for i in result:
                if i == "food_name" or i == "brand_name":
                    continue
                value = result[i]
                sectionTitle = i
                if "_" in sectionTitle:
                    sectionTitle = sectionTitle.replace("_", " ")
                if "nf " in sectionTitle:
                    sectionTitle = sectionTitle.replace("nf ", "")
                sectionTitle = sectionTitle.title()

                if columnCounter%3==0:
                    fi1.html(f"<p style='font-weight: 600; margin:0'>{sectionTitle}</p><p>{value}</p>")
                elif columnCounter%3==1:
                    fi2.html(f"<p style='font-weight: 600; margin:0'>{sectionTitle}</p><p>{value}</p>")
                else:    
                    fi3.html(f"<p style='font-weight: 600; margin:0'>{sectionTitle}</p><p>{value}</p>")

                columnCounter+=1

                if sectionTitle == "P":
                    break
            time.sleep(3)
            foundMessage.empty()
    except Exception as e:
        st.error("Oh no! The food you input was not found. Try again.", icon="❗")
#-----------------------------------------------------------------------

#----------------------------------------------------Main Webpage Code----------------------------------------------------
messages = []
file = open("longMessages.txt", "r")
while True:
    content = file.readline()
    messages.append(content)
    if not content:
        break
file.close()

st.sidebar.header("Click on where to go", divider="gray")

pageSelection = st.sidebar.selectbox("Choose where to go next.", ("Home", "About", "Code Breakdown",), label_visibility="collapsed")
if pageSelection == "Home":
    # Title and caption introducing the user to the website
    st.title("Health and Nutrition Assistant")

    # Form for user to input all their health information
    st.header("Enter Your Health Information", divider="gray")

    # Sex selectbox
    st.write("**Sex**")
    sex = st.selectbox('Sex', ("","Male", "Female"), label_visibility="collapsed")

    # Date of birth date input
    st.write("**Date of Birth**")
    dob = st.date_input("Date of Birth", None, datetime.date(1904,1,1), datetime.date(2023, today.month, today.day-1), format="MM/DD/YYYY", label_visibility="collapsed")

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
    activity = st.radio("Activity Level", ("Inactive","Low Active", "Active", "Very Active"), None, label_visibility="collapsed", horizontal=True)

    # This check if the form was submitted    
    if sex!="" and dob!=None and feet!=0 and weight!=0.00 and activity!=None:
        st.subheader("Body Mass Index Information")
        renderUserInputTable(dob, sex, feet, inches, weight, activity)
        renderBMI(feet, inches, weight)

        st.divider()

        st.subheader("Choose What to See Next")
        sectionSelection = st.selectbox("Choose What to See Next", ["", "Nutrition Breakdown and Recommendations", "Food Intake Analysis and Recommendations"], label_visibility="collapsed")

        st.divider()

        if sectionSelection == "Nutrition Breakdown and Recommendations":
            renderNutrition(sex.lower(), ageCalculator(dob), feet, inches, weight, activity)
        elif sectionSelection == "Food Intake Analysis and Recommendations":
            renderFoodIntake()
elif pageSelection == "About":
    st.title("About")
    st.header("Purpose of the website", divider="gray")
    st.write(messages[0])

    st.header("Alright I got nutrition, what about exercise?", divider="gray")
    st.write(messages[1])
    btn11, btn12, btn13 = st.columns(3)
    btn21, btn22, btn23 = st.columns(3)

    btn11.link_button("r/BeginnerFitness", "https://www.reddit.com/r/beginnerfitness/", use_container_width=True)
    btn12.link_button("Stronger By Science", "https://www.strongerbyscience.com/", use_container_width=True)
    btn13.link_button("The Fitness Wiki", "https://thefitness.wiki/routines/", use_container_width=True)
    btn21.link_button("ExRx", "https://exrx.net/", use_container_width=True)
    btn22.link_button("USDA", "https://www.nutrition.gov/topics/exercise-and-fitness", use_container_width=True)
    btn23.link_button("American Council on Exercise", "https://www.acefitness.org/resources/everyone/exercise-library/", use_container_width=True)
elif pageSelection == "Code Breakdown":
    st.title("Code Breakdown")
    st.header("APIs Used", divider="gray")

    st.subheader("Nutrition Calculator")
    st.write("Provided the user's recommended nutrional intake using formulas from the US Health and Medicine Division of the National Academies of Sciences, Engineering and Medicine.")
    st.link_button("Go to API Page", "https://rapidapi.com/sprestrelski/api/nutrition-calculator")

    st.subheader("Nutritionix")
    st.write("Provided a database of foods and their respective nutritonal composition.")
    st.link_button("Go to API Page", "https://www.nutritionix.com/")

    st.header("Design Choices", divider="gray")
    st.write(messages[2])
    bigCode = '''bmiURL = calculatorURL + "/bmi"
    querystring = {"measurement_units":"std","feet":f"{feet}","inches":f"{inches}","lbs":f"{int(weight)}"}
    bmiRequest = requests.get(bmiURL, headers=calculatorHeaders, params=querystring).json()

    bmiValue = '{0:.1f}'.format(float(bmiRequest["bmi"]))

    st.write(f"Your BMI is **{bmiValue}** which means you fall into the {bmiStringReturn(float(bmiValue))} category.")
    st.image("bmiChart.jpg")
'''
    st.code(bigCode, language="python")

    st.write(messages[3])
    simpleCode = '''renderBMI(feet, inches, weight)'''
    st.code(simpleCode, language="python")

    st.write(messages[4])
    longCode = f'''{messages[1]}'''
    st.code(longCode, language="None")

    st.write(messages[5])
    st.code('''st.write(messages[1])''', language="Python")

    homeCodeTogether = ''' st.title("Health and Nutrition Assistant")
    st.header("Enter Your Health Information", divider="gray")
    st.write("**Sex**")
    sex = st.selectbox('Sex', ("","Male", "Female"), label_visibility="collapsed")
    st.write("**Date of Birth**")
    dob = st.date_input("Date of Birth", None, datetime.date(1904,1,1), datetime.date(2023, today.month, today.day-1), format="MM/DD/YYYY", label_visibility="collapsed")
    st.write("**Height**")
    col1, col2 = st.columns(2)
    col1.write("Feet")
    feet = col1.number_input("Feet", 0, 8, label_visibility="collapsed")
    col2.write("Inches")
    inches = col2.number_input("Inches", 0, 11, label_visibility="collapsed")
    st.write("**Weight**")
    weight = st.number_input("Weight", 0.0, 500.0, "min", 0.1, label_visibility="collapsed")
    st.write("**Activity Level**")
    activity = st.radio("Activity Level", ("Inactive","Low Active", "Active", "Very Active"), None, label_visibility="collapsed", horizontal=True)'''
    st.write(messages[6])
    st.code(homeCodeTogether, language="Python")

    st.write(messages[7])

    homeCode = ''' # Title and caption introducing the user to the website
    st.title("Health and Nutrition Assistant")

    # Form for user to input all their health information
    st.header("Enter Your Health Information", divider="gray")

    # Sex selectbox
    st.write("**Sex**")
    sex = st.selectbox('Sex', ("","Male", "Female"), label_visibility="collapsed")

    # Date of birth date input
    st.write("**Date of Birth**")
    dob = st.date_input("Date of Birth", None, datetime.date(1904,1,1), datetime.date(2023, today.month, today.day-1), format="MM/DD/YYYY", label_visibility="collapsed")

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
    activity = st.radio("Activity Level", ("Inactive","Low Active", "Active", "Very Active"), None, label_visibility="collapsed", horizontal=True)
'''
    st.code(homeCode, language="Python")
    
    st.write(messages[8])