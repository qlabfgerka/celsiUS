from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
#import decisiontree
from datetime import datetime, timedelta
import pandas as pd
import requests
import model
import numpy as np





app = Flask(__name__)
CORS(app, support_credentials=True)

bigBrain = None
bigSc = None

# humidity = current humidity
# people = people home (YES/NO)
# warmDay = YES/NO
# warmNight = YES/NO
# windowOpen = YES/NO

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


@app.before_first_request
def activate_job():
    print("before")
    (b, s) = model.neuralnetwork()
    global bigBrain
    global bigSc
    bigBrain = b
    bigSc = s



@app.route('/predict', methods=['GET'])
@cross_origin(supports_credentials=True)
def predict():
    args = request.args.to_dict()
    now = ceil_dt(datetime.now(), timedelta(minutes=30))
    current_time = now.strftime("%H:%M")
    print("args", args)

    response = requests.get('http://api.weatherapi.com/v1/history.json?key=1874708dfaad4509b83165632221705&q=Ljubljana&dt=%s' % (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")).json()

    temperatures = response["forecast"]["forecastday"][0]["hour"]

    result = list(map(lambda x: x["temp_c"], temperatures))[:16]

    print(result)

    #make call to temp prediction
    predictedTemp = model.predict(bigBrain, bigSc, np.array(result))

    print(result)
    print(predictedTemp)

    # make obj
    data = pd.DataFrame(index=pd.Index([1]), data = {'Temperature': predictedTemp,
                        'People home': args.get("people"),
                        'Ura': current_time,
                        'Vlaznost': args.get("humidity"),
                        'Warm Day': args.get("warmDay"),
                        'Warm Night': args.get("warmNight"),
                        'Window open': args.get("windowOpen")})

    print("data:", data)

    

    return jsonify({'decision': decisiontree.predict(data)})


if __name__ =='__main__':
    app.run(debug = True)  