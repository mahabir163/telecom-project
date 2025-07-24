import sys
import numpy as np
import pandas as pd
import pickle
import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password="",   
    database="telecom"
)

class CustomData:
    def __init__(self,gender, 
                 SeniorCitizen:int, Partner, Dependents, tenure, PhoneService, 
                 MultipleLines, InternetService, OnlineSecurity, OnlineBackup, 
                 DeviceProtection, TechSupport, StreamingTV, StreamingMovies, 
                 Contract, PaperlessBilling, PaymentMethod, MonthlyCharges:float, 
                 TotalCharges:float):
        self.gender = gender
        self.SeniorCitizen = SeniorCitizen
        self.Partner = Partner
        self.Dependents = Dependents
        self.tenure = tenure
        self.PhoneService = PhoneService
        self.MultipleLines = MultipleLines
        self.InternetService = InternetService
        self.OnlineSecurity = OnlineSecurity
        self.OnlineBackup = OnlineBackup
        self.DeviceProtection = DeviceProtection
        self.TechSupport = TechSupport
        self.StreamingTV = StreamingTV
        self.StreamingMovies = StreamingMovies
        self.Contract = Contract
        self.PaperlessBilling = PaperlessBilling
        self.PaymentMethod = PaymentMethod
        self.MonthlyCharges = MonthlyCharges
        self.TotalCharges = TotalCharges
    
    def convert_to_dataframe(self):
        try:
            custom_data_input = {
                "gender" : [self.gender],
                "SeniorCitizen" : [self.SeniorCitizen],
                "Partner" : [self.Partner],
                "Dependents" : [self.Dependents],
                "tenure" : [self.tenure],
                "PhoneService"  : [self.PhoneService],
                "MultipleLines" : [self.MultipleLines], 
                "InternetService"  : [self.InternetService],
                "OnlineSecurity" : [self.OnlineSecurity], 
                "OnlineBackup"  : [self.OnlineBackup],
                "DeviceProtection": [self.DeviceProtection],  
                "TechSupport"  : [self.TechSupport],
                "StreamingTV" : [self.StreamingTV], 
                "StreamingMovies" : [self.StreamingMovies], 
                "Contract"  : [self.Contract],
                "PaperlessBilling" : [self.PaperlessBilling], 
                "PaymentMethod" : [self.PaymentMethod], 
                "MonthlyCharges": [self.MonthlyCharges], 
                "TotalCharges" : [self.TotalCharges] 
            }
            return pd.DataFrame(custom_data_input)
        except Exception as e:
            raise e

model_path = r"artifacts\model.pkl"
pre_pros_path = r"artifacts\preprocessor.pkl"

class Prediction:
    def predict(self,input_feature):
        try:
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            with open(pre_pros_path,"rb") as fileobj:
                preprocessor = pickle.load(fileobj)
        
            data_scaled = preprocessor.transform(input_feature)
            pred = model.predict(data_scaled)
            pred_proba = model.predict_proba(data_scaled).astype("float32")
            pred_proba = pred_proba[0][1]
            va = round(pred_proba,2) * 100
            val = str(va)
            
            if pred_proba <= 1 and pred_proba >= 0.9:
                comment = f"Churn probability: {val}% This customer is at high risk of discontinuing our services within the next few months. Kindly reach out to them immediately, provide special offers or cashback, and assure them that our team is committed to continuously improving our services."

            elif pred_proba < 0.9 and pred_proba >= 0.7:
                comment = f"Churn probability: {val}% This customer has a very high likelihood of leaving our service in the next few months. Immediate action is required — please contact them personally, offer exclusive discounts, cashback, or special deals, and assure them that our team is committed to improving their experience. Understanding their concerns through direct feedback can help us retain them effectively."
            elif pred_proba < 0.7 and pred_proba >= 0.5:
                comment = f"Churn probability: {val}% The customer is at high risk of discontinuing our services. Proactive engagement is necessary — reach out via personalized email, SMS, or calls, offering attractive deals, loyalty rewards, or small cashback options. Gathering their feedback through surveys can also reveal areas where we need to improve."
            elif pred_proba < 0.5 and pred_proba >= 0.2:
                comment = f"Churn probability: {val}% This customer shows moderate signs of potential churn, but the situation can still be controlled. It's advisable to keep them engaged by sending useful information, appreciation messages, or offering minor incentives like bonus features. Encouraging them to share feedback will help us identify their needs early."
            elif pred_proba < 0.4 and pred_proba >= 0.0:
                comment = f"Churn probability: {val}% The customer is currently loyal with a very low risk of leaving our service. We should maintain this positive relationship by occasionally sending thank-you messages, service updates, or exclusive previews of upcoming features. Encouraging them to refer others or leave positive reviews can further strengthen loyalty."

            return (pred,comment,pred_proba)
        except Exception as e:
            raise e
        
    
