import streamlit as st
from prediction_helper import predict

st.title("Health Insurance cost Prediction")

categorical_options = {
    'gender' : ['Male', 'Female'],
    'region' : ['Northwest', 'Northeast', 'Southeast', 'Southwest'],
    'marital_status' : ['Unmarried', 'Married'],
    'bmi_category' : ['Normal', 'Overweight', 'Underweight', 'Obesity'],
    'smoking_status' : ['No Smoking', 'Regular', 'Occasional'],
    'employment_status' : ['Salaried', 'Self-Employed', 'Freelancer'],
    'income_level' : ['<10L', '> 40L', '10L - 25L', '25L - 40L'],
    'medical_history' : ['Diabetes', 'High blood pressure', 'No Disease', 'Heart disease',
     'Diabetes & High blood pressure', 'Diabetes & Thyroid',
     'Diabetes & Heart disease', 'High blood pressure & Heart disease',
     'Thyroid'],
    'insurance_plan' : ['Bronze', 'Silver', 'Gold']
}

#create 4 rows of 3 columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Assign inputs to the grid
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100)
with row1[1]:
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20)
with row1[2]:
    income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)

with row2[0]:
    genetical_risk = st.number_input('Genetical Risk', step=1, min_value=0, max_value=5)
with row2[1]:
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['insurance_plan'])
with row2[2]:
    employment_status = st.selectbox('Employment Status', categorical_options['employment_status'])

with row3[0]:
    gender = st.selectbox('Gender', categorical_options['gender'])
with row3[1]:
    marital_status = st.selectbox('Marital Status', categorical_options['marital_status'])
with row3[2]:
    bmi_category = st.selectbox('BMI Category', categorical_options['bmi_category'])

with row4[0]:
    smoking_status = st.selectbox('Smoking Status', categorical_options['smoking_status'])
with row4[1]:
    region = st.selectbox('Region', categorical_options['region'])
with row4[2]:
    medical_history = st.selectbox('Medical History', categorical_options['medical_history'])
# Create a dictionary for input values
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}


if st.button("Predict"):
    prediction = predict(input_dict)
    st.success(f"Predicted Premium: {prediction}")