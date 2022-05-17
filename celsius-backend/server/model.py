import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import pickle

def neuralnetwork():
    print("neural network")

    # data load and preprocessing data
    weather = pd.read_csv("./2953968.csv", index_col="DATE")
    core_weather = weather[["PRCP", "TMAX", "TMIN"]].copy()
    core_weather.columns = ["precip", "temp_max", "temp_min"]
    core_weather = core_weather.fillna(method="ffill")
    core_weather = core_weather.iloc[:-1, :].copy()
    core_weather["target"] = core_weather.shift(-1)["temp_max"]
    core_weather = core_weather.fillna(method="ffill")

    dataset = core_weather["temp_max"]
    dataset_to_numpy = core_weather["temp_max"].to_numpy()
    #training_set = dataset_to_numpy[13550:48140]
    training_set = dataset_to_numpy

    training_set = np.array(training_set)
    training_set = training_set.reshape(-1, 1)
    copy_set = training_set

    # Next, we will have to apply feature scaling to normalize temperature in the range 0 to 1.
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # we will create a training set for every 30 hours since those are the cycles of the hours and for 4 hour prediction
    x_train = []
    y_train = []

    n_future = 1  # next 12 hours
    n_past = 16  # Past 12 hours

    for i in range(0, len(training_set_scaled) - n_past - n_future + 1):
        x_train.append(training_set_scaled[i: i + n_past, 0])
        y_train.append(training_set_scaled[i + n_past: i + n_past + n_future, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #here is our rnn model which uses training data provided to learn

    regressor = Sequential()
    regressor.add(Bidirectional(LSTM(units=30, return_sequences=True, input_shape=(x_train.shape[1], 1))))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30, return_sequences=True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30, return_sequences=True))
    regressor.add(Dropout(0.2))
    regressor.add(LSTM(units=30))
    regressor.add(Dropout(0.2))
    regressor.add(Dense(units=n_future, activation='linear'))
    regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])
    regressor.fit(x_train, y_train, epochs=1, batch_size=32)
    return (regressor, sc)


#now the test dataset
def predict(regressor, sc, previous_16_h):
    testdata = previous_16_h
    testdata = testdata.reshape(-1, 1)
    
    testing = sc.transform(testdata)
    testing = np.array(testing)
    testing = np.reshape(testing, (testing.shape[1], testing.shape[0], 1))

    predicted_temperature = regressor.predict(testing)
    predicted_temperature = sc.inverse_transform(predicted_temperature)
    predicted_temperature = np.reshape(predicted_temperature,(predicted_temperature.shape[1],predicted_temperature.shape[0]))

    print("predicted temp\n")
    print(predicted_temperature)
    return predicted_temperature[0]


