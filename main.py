from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    try:
        import joblib
        import pandas as pd
        import numpy as np
        model=joblib.load("mymodel.h5")
        f=model.feature_names_in_
        g={
        "GPA" : float(request.form['GPA']),
        "SAT_Score" : int(request.form['SAT_Score']),
        "Study_Hours_Per_Week" : int(request.form['Study_Hours_Per_Week']),
        "Parent_Education" : request.form['Parent_Education'],
        "Extracurricular_Participation" : request.form["Extracurricular_Participation"],
        "Motivation_Level" :request.form['Motivation_Level'],
        "Home_Environment" : request.form['Home_Environment']
        }
        g=pd.DataFrame([g])
        g=pd.get_dummies(g)
        g=g.reindex(columns=f,fill_value=0)
        r=model.predict(g)
        if r[0]=='Bad':
            result=0
        elif r[0]=='Good':
            result=1
        else:
            result=-1
        
    except ValueError:
        result = "Invalid input! Please enter numbers only."
    
    return redirect(url_for('result', result=result))
    print("result")

@app.route('/result')
def result():
    result = request.args.get('result')
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True,port=8080)

