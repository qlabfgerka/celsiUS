import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
from sklearn.preprocessing import MinMaxScaler


def rrm():
    print("Ridge regression model")
    # weather = pd.read_csv("2953976.csv", index_col="DATE")
    weather = pd.read_csv("../../../celsiUS/celsius-backend/ml/2953968.csv", index_col="DATE")
    # print(weather)

    # DATA PREPROCESSING
    # finding missing values
    # out = weather.apply(pd.isnull).sum() / weather.shape[0]
    # print(out)

    # taking only importat columns and renaming them
    core_weather = weather[["PRCP", "TMAX", "TMIN"]].copy()
    core_weather.columns = ["precip", "temp_max", "temp_min"]

    # filling in missing Values
    # we are gonna fill them with forward fill
    core_weather = core_weather.fillna(method="ffill")

    # print(core_weather)
    # out = core_weather.apply(pd.isnull).sum() / core_weather.shape[0]
    # print(out)
    # print(core_weather.dtypes)

    core_weather.index = pd.to_datetime(core_weather.index)
    # print(core_weather.index)

    # machine learning model to predict tempmax for next hour
    # getting rid of the last row so NaN doesnt appear
    core_weather = core_weather.iloc[:-1, :].copy()
    core_weather["target"] = core_weather.shift(-1)["temp_max"]
    core_weather = core_weather.fillna(method="ffill")
    #print(core_weather)


    reg = Ridge(alpha=.1)
    predictors = ["precip", "temp_max", "temp_min"]

    #training set, up to the date provided
    train = core_weather.loc[:"2019-01-01"]
    #test set, from the date onward
    test = core_weather.loc["2021-11-29":]

    reg.fit(train[predictors], train["target"])
    predictions = reg.predict(test[predictors])

    error = mean_absolute_error(test["target"], predictions)
    print(error)

    #lets see actuals and predictions
    comparison = pd.concat([test["target"], pd.Series(predictions, index=test.index)], axis=1)
    comparison.columns = ["actual", "predictions"]
    print(comparison)

def neuralnetwork():
    print("neural network")

    # data load and preprocessing data
    weather = pd.read_csv("../../../celsiUS/celsius-backend/ml/2953968.csv", index_col="DATE")
    core_weather = weather[["PRCP", "TMAX", "TMIN"]].copy()
    core_weather.columns = ["precip", "temp_max", "temp_min"]
    core_weather = core_weather.fillna(method="ffill")
    core_weather = core_weather.iloc[:-1, :].copy()
    core_weather["target"] = core_weather.shift(-1)["temp_max"]
    core_weather = core_weather.fillna(method="ffill")

    dataset = core_weather["temp_max"]
    dataset_to_numpy = core_weather["temp_max"].to_numpy()
    training_set = dataset_to_numpy[13550:48140]
    training_set = training_set.reshape(-1, 1)
    print(training_set)

    #now the test data

    # Next, we will have to apply feature scaling to normalize temperature in the range 0 to 1.
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # we will create a training set for every 30 hours since those are the cycles of the hours and for 4 hour prediction
    x_train = []
    y_train = []

    n_future = 4  # next 4 hours
    n_past = 30  # Past 30 hours

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
    regressor.fit(x_train, y_train, epochs=3, batch_size=32)


    #now the test dataset
    testdata = dataset_to_numpy
    real_temp = dataset_to_numpy
    testdata = testdata.reshape(-1, 1)
    real_temp = real_temp.reshape(-1, 1)

    testing = sc.transform(testdata)
    testing = np.array(testing)
    testing = np.reshape(testing, (testing.shape[1], testing.shape[0], 1))

    predicted_temperature = regressor.predict(testing)
    predicted_temperature = sc.inverse_transform(predicted_temperature)
    predicted_temperature = np.reshape(predicted_temperature,(predicted_temperature.shape[1],predicted_temperature.shape[0]))

    print(real_temp)
    print(predicted_temperature)

#rrm()
neuralnetwork()