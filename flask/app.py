from flask import Flask, render_template, request, url_for
import pandas as pd 
import numpy as np
import pickle
 
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict(inf_factor = 1.1):
    
    with open('model.pkl', 'rb') as f:
        reg = pickle.load(f)
    
    if request.method == 'POST':
        data = request.form

        try:
            sqft = int(data['sqft'])
        except ValueError:
            sqft = 1000
        
        z = data['zip']
        cols = pd.read_csv("columns.csv")
        house = np.zeros([1,len(cols)])
        house[0,-1] += sqft
        
        haszip = False
        for i, c in enumerate(cols.values):
            if z==c[0]:
                haszip = True
                house[0,i] = 1
        if haszip == False:
            #if zip not in model, it defaults to 96010
            idx = np.argmax(cols.values=='96010')
            house[0,idx] = 1
            
        pred = int(np.round(reg.predict(house)*inf_factor, -3))

    return render_template('result.html', zip_ = z,
        sqft = sqft, prediction = pred, zips = np.array(cols[2:-1]))


if __name__ == '__main__':
    app.run(debug=True)