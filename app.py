from flask import Flask,render_template,request
import mysql.connector
from src.predPipeline import CustomData,Prediction


mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password="",   
    database="telecom"
)
cursor = mydb.cursor()
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def log_in():
    if(request.method == "POST"):
        u_name = request.form["username"]
        password = request.form["password"]
        sql = "SELECT EXISTS(SELECT 1 FROM customer_executive WHERE id = %s and password = %s)"
        values = (u_name,password)
        cursor.execute(sql,values)
        exists = cursor.fetchone()[0]

        if exists:
            print("Value exists in the database.")
            return render_template("index.html",u_name = u_name)
        else:
            print("Wrong username or password!! Contact to admin")
            val = "* Wrong username or password!! Contact to admin"
            return render_template("login.html",val=val)
    return render_template("login.html", val="")



@app.route("/submit",methods=["GET","POST"])
def take_input():
    
    customerName = request.form["customerName"]
    customerMobile = request.form["customerMobile"]
    customerID = request.form["customerID"]
    gender = request.form["gender"]
    SeniorCitizen = request.form["SeniorCitizen"]
    Partner = request.form["Partner"]
    Dependents = request.form["Dependents"]
    tenure = request.form["tenure"]
    PhoneService = request.form["PhoneService"]
    MultipleLines = request.form["MultipleLines"]
    InternetService = request.form["InternetService"]
    OnlineSecurity = request.form["OnlineSecurity"]
    OnlineBackup = request.form["OnlineBackup"]
    DeviceProtection  = request.form["DeviceProtection"]
    TechSupport = request.form["TechSupport"]
    StreamingTV = request.form["StreamingTV"]
    StreamingMovies = request.form["StreamingMovies"]
    Contract = request.form["Contract"]
    PaperlessBilling = request.form["PaperlessBilling"]
    PaymentMethod = request.form["PaymentMethod"]
    MonthlyCharges = request.form["MonthlyCharges"]
    TotalCharges = request.form["TotalCharges"]
    if SeniorCitizen == "Yes":
        SeniorCitizen = 0
    else :
        SeniorCitizen = 1
    
    data = CustomData(gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges)
    pred_df = data.convert_to_dataframe()
    print(pred_df)

    model = Prediction()
    res,comment,prob = model.predict(pred_df)
    sql = "INSERT INTO churn_information VALUES(%s,%s,%s,%s,%s)"
    values = (customerID,customerName,customerMobile,float(prob),comment)
    cursor.execute(sql,values)
    mydb.commit()
    print(res)
    return render_template("index.html",res=res[0],recom=comment)




if __name__ == "__main__":
    app.run(host="0.0.0.0")