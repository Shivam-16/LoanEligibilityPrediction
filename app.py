# Project: Loan Eligibility Prediction System

from flask import Flask, render_template, request, jsonify
from sklearn import tree
import pandas as pd
import pickle
import os

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/loan", methods=['POST'])
def loan_eligibilty():
    # Predicting with our Decision Tree
    with open('models/best_model.pkl', 'rb') as f:
        best_model = pickle.load(f)
    
    gend = 1 if request.form["gender"] == "Male" else 0
    married = 1 if request.form["married"] == "Yes" else 0
    dependents = request.form["dependents"]
    education = 1 if request.form["education"] == "Graduate" else 0
    self_employed = 1 if request.form["self_employed"] =="Yes" else 0
    applicant_income = request.form['applicantincome']
    co_applicant_income = request.form["coapplicantincome"]
    loan_amount = request.form["loanamount"]
    loan_amount_term = request.form["loanamountterm"]
    credit_history = request.form["credithistory"]
    property_area = request.form["propertyarea"]
    if property_area == "Urban":
        property_area = 0
    elif property_area == "Rural":
        property_area = 1
    else:
        property_area = 2
    cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
       'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    df = pd.DataFrame([[gend, married, dependents, education, self_employed, applicant_income, co_applicant_income, loan_amount, loan_amount_term, credit_history,property_area]],columns=cols)
    print(df.values)
    result = best_model.predict(df)
    print(result)
    if result[0] =='Y':
        return render_template('result.html', result= "We're happy to share you that you are ELIGIBLE.")
    return render_template('result.html', result="We're sad to share you that you are NOT ELIGIBLE.")

@app.route("/input_show", methods=['POST'])
def show_inputs():
    if request.method == 'POST':
        gend = request.form["gender"]
        married = request.form["married"]
        dependents = request.form["dependents"]
        education = request.form["education"]
        self_employed = request.form["self_employed"]
        applicant_income = request.form['applicantincome']
        co_applicant_income = request.form["coapplicantincome"]
        loan_amount = request.form["loanamount"]
        loan_amount_term = request.form["loanamountterm"]
        credit_history = request.form["credithistory"]
        property_area = request.form["propertyarea"]
        final_ = f'''The input you have provided is:
                Gender: {gend},
                Married: {married},
                Dependents: {dependents},
                Education: {education},
                Self_Employed: {self_employed},
                Applicant_Income: {applicant_income},
                Co-Applicant Income: {co_applicant_income},
                Loan Amount: {loan_amount},
                Loan Amount Term: {loan_amount_term},
                Credit History: {credit_history},
                Property Area: {property_area}       
                '''
        return render_template('stage.html', result = final_)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)