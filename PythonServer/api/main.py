from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"Greetings": "Welcome to blah blah"}

class Diagnosis(BaseModel):
    age: str
    gender: str
    married: str
    symptoms: str

@app.post("/sendData")
async def predict_Allergy(Data:Diagnosis):
    import json
    # flag="This is funnny"
    # print('request recieved')
    # return json.dumps(flag)


# FINAL ML CORRECT CODE
    import numpy as np
    import pandas as pd
    import re

    pid = -1
    x=False

    while(x==False):   
        if(x==False):
            # age = input("Write your age(only whole number): ")
            if ((Data.age).isnumeric()):
                int(Data.age)
                x = True
            else:
                x=False

    import csv
    f = open('C:/Users/Abc/PythonServer/PatientsData.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        pid = pid+1

        #loading data
    data = pd.read_csv(r"C:/Users/Abc/PythonServer/PatientsData.csv", encoding='latin 1')

    data.loc[pid] = [pid,Data.age,Data.gender,Data.married,Data.symptoms,'', '', '']
    # data.tail()
    data["Age"] = pd.to_numeric(data["Age"])

    #replacing missing values with mean
    Mean = round(data['Age'].mean())
    data['Age'].fillna(value=Mean, inplace=True)

    #applying row filter on age
    data_row = data.Age >= 0
    data = data[data_row]
    data_row = data.Age <= 70
    data = data[data_row]

    #removing useless columns
    data = data.drop(columns="RACE_FACTOR")
    data = data.drop(columns="ETHNICITY_FACTOR")

    target = data['Target_Label']

    inputs = pd.DataFrame(data)
    inputs = inputs.rename(columns={"marital_status": "MaritalStatus"})

    #categorical to continuous conversion
    from sklearn.preprocessing import LabelEncoder
    le_Gender = LabelEncoder()
    le_MaritalStatus = LabelEncoder()
    le_Symptoms = LabelEncoder()

    inputs['Gender_n'] = le_Gender.fit_transform(inputs['Gender'])
    inputs['MaritalStatus_n'] = le_MaritalStatus.fit_transform(inputs['MaritalStatus'])
    inputs['Symptoms_n'] = le_Symptoms.fit_transform(inputs['Symptoms'])

    new_age = inputs['Age'].values[pid]
    new_gender = inputs['Gender_n'].values[pid]
    new_maritalstatus = inputs['MaritalStatus_n'].values[pid]
    new_symptom = inputs['Symptoms_n'].values[pid]
    # print(new_age, new_gender, new_maritalstatus, new_symptom)

    inputs = inputs[inputs.Patient_ID != pid]
    data = data.iloc[:-1] 
    target = target.iloc[:-1] 

    inputs_n = inputs.drop(['Patient_ID', 'Gender', 'MaritalStatus', 'Symptoms'], axis='columns')

    X = inputs_n[['Age', 'Gender_n', 'MaritalStatus_n', 'Symptoms_n']]

    #partitioning data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test  = train_test_split(X, target, random_state=500)

    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.metrics import accuracy_score
    gb = GradientBoostingClassifier(n_estimators=4000, learning_rate = 0.05)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)
    y_pred=y_test
    accuracy_score(y_pred, gb_pred)

    Xnew = [[new_age, new_gender, new_maritalstatus, new_symptom]]
    Xnewpred = gb.predict(Xnew)
    print(Xnewpred)

    return json.dumps(Xnewpred[0])
