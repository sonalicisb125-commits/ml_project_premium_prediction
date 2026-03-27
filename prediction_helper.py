import pandas as pd
from joblib import load

model_rest = load("artifacts/model_resr.joblib")
model_young = load("artifacts/model_young.joblib")

scaler_rest = load("artifacts/scaler_rest.joblib")
scaler_young = load("artifacts/scaler_young.joblib")


def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    # Step 1: Split diseases
    diseases = medical_history.lower().split("&")

    # Step 2: Clean spaces
    diseases = [d.strip() for d in diseases]

    # Step 3: Handle single disease (ensure 2 values like your dataframe logic)
    if len(diseases) == 1:
        diseases.append("none")

    # Step 4: Calculate total risk score
    total_score = 0
    for d in diseases:
        total_score += risk_scores.get(d, 0)  # default 0 if not found

    # Step 5: Normalize (IMPORTANT: use same min/max from training)
    min_score = 0
    max_score = 16  # max possible (8 + 8)

    normalized_score = (total_score - min_score) / (max_score - min_score)

    return normalized_score

def preprocess_input(input_dict):
    expected_columns = ['age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
     'genetical_risk', 'normalize_risk_score', 'gender_Male',
     'region_Northwest', 'region_Southeast', 'region_Southwest',
     'marital_status_Unmarried', 'bmi_category_Obesity',
     'bmi_category_Overweight', 'bmi_category_Underweight',
     'smoking_status_Occasional', 'smoking_status_Regular',
     'employment_status_Salaried', 'employment_status_Self-Employed']

    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}

    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    # df.fillna(0, inplace=True)

    # Manually assign values for each categorical input based on input_dict
    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':  # Correct key usage with case sensitivity
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'Age':  # Correct key usage with case sensitivity
            df['age'] = value
        elif key == 'Number of Dependants':  # Correct key usage with case sensitivity
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':  # Correct key usage with case sensitivity
            df['income_lakhs'] = value
        elif key == "Genetical Risk":
            df['genetical_risk'] = value

    df['normalize_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    df = handle_scaling(input_dict['Age'], df)
    return df

def handle_scaling(age, df):
    if age <=27:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level']=None
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis=1, inplace=True)
    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)


    if input_dict["Age"] <= 27:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])