from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib
import os 
import pickle 

from xgboost import XGBRegressor

app = Flask(__name__)

# Loading the pre-trained model
path=os.path.dirname(os.path.abspath(__file__))
rec = joblib.load(os.path.join(path,'D:/i2_final/HRec/HRec.pkl'))

# the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# the route for the prediction page
@app.route('/predict', methods=['POST'])
def prediction():
    # input values from user
    ra= float(request.form['ra'])
    d= int(request.form['d'])
    re = float(request.form['re'])
    s= float(request.form['s'])
    p=int(request.form['p'])
    t=float(request.form['t'])

    state=request.form['state']
    if(state=='Banglore'):
        Banglore=1.0
        Chennai=0.0
        Delhi=0.0
        Hyderabad=0.0
        Kolkata=0.0
        Mumbai=0.0

    elif(state=='Chennai'):
        Banglore=0.0
        Chennai=1.0
        Delhi=0.0
        Hyderabad=0.0
        Kolkata=0.0
        Mumbai=0.0

    elif (state=='Delhi'):
        Banglore=0.0
        Chennai=0.0
        Delhi=1.0
        Hyderabad=0.0
        Kolkata=0.0
        Mumbai=0.0

    elif (state=='Hyderabad'):
        Banglore=0.0
        Chennai=0.0
        Delhi=0.0
        Hyderabad=1.0
        Kolkata=0.0
        Mumbai=0.0

    elif (state=='Kolkata'):
        Banglore=0.0
        Chennai=0.0
        Delhi=0.0
        Hyderabad=0.0
        Kolkata=1.0
        Mumbai=0.0

    elif (state=='Mumbai'):
        Banglore=0.0
        Chennai=0.0
        Delhi=0.0
        Hyderabad=0.0
        Kolkata=0.0
        Mumbai=1.0

    

    # Predict the hotel using the pre-trained model
    ip=np.array([[Banglore,Chennai,Delhi, Hyderabad, Kolkata, Mumbai,ra,d,re,s,p,t]])
    predicted_Hrec= rec.predict(ip)[0]

    df=pd.read_csv( 'hotel_data.csv')
    predicted_Hrec1=df.loc[int(predicted_Hrec)]
    print(predicted_Hrec1)
    c=['Hotel Name','Rating', 'Rating Description', 'Reviews', 'Star Rating', 'Location', 'Price','Tax']
    data1= [{'column': column, 'value': predicted_Hrec1[column]} for column in c]

    # Rendering the result page with predicted value
    return render_template('index.html', predicted_Hrec1=data1)


if __name__ == '__main__':
    app.run(debug=True)
