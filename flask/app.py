from flask import Flask, render_template, request, url_for

import pandas as pd 
import numpy as np
import pickle
 
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    with open('model.pkl', 'rb') as f:
        reg = pickle.load(f)
    
    if request.method == 'POST':
        data = request.form

        try:
            sqft = int(data['sqft'])
        except ValueError:
            sqft = 0
        
        z = data['zip']
        cols = pd.read_csv("columns.csv")
        house = np.zeros([1,len(cols)])
        house[0,0] += sqft

        for i, c in enumerate(cols.values):
            if z==c[0]: house[0,i] = 1
    
    return render_template('result.html', zipcode = z, sqft = sqft,
        prediction = int(reg.predict(house)))


if __name__ == '__main__':
    app.run(debug=True)