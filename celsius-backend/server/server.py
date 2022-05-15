from flask import Flask, request
import decisiontree
from datetime import datetime, timedelta
import pandas as pd


app = Flask(__name__)

# temperature = current temperature
# humidity = current humidity
# people = people home (YES/NO)
# warmDay = YES/NO
# warmNight = YES/NO
# windowOpen = YES/NO

def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

@app.route('/predict', methods=['GET'])
def predict():
    args = request.args.to_dict()
    now = ceil_dt(datetime.now(), timedelta(minutes=30))
    current_time = now.strftime("%H:%M")
    print("args", args)


    #make call to temp prediction

    # make obj
    data = pd.DataFrame(index=pd.Index([1]), data = {'Temperature': args.get("temperature"),
                        'Predicted Temperature +1h': 15,
                        'People home': args.get("people"),
                        'Ura': current_time,
                        'Vlaznost': args.get("humidity"),
                        'Warm Day': args.get("warmDay"),
                        'Warm Night': args.get("warmNight"),
                        'Window open': args.get("windowOpen")})

    print("data:", data)

    return decisiontree.predict(data)


if __name__ =='__main__':  
    app.run(debug = True)  