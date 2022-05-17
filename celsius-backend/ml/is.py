import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import pickle

def showData(history):
    print(f"model hist is : \n {history.history}")

    plt.subplot(2, 1, 1)
    plt.title("Accuracy/Loss")
    plt.plot(history.history['acc'], label="Test Accuracy")
    #plt.plot(testHistoryAccuracy, label="Train Accuracy")
    plt.legend(loc='lower right')
    plt.ylim([0, 1.0])

    plt.subplot(2, 1, 2)
    plt.plot(history.history['loss'], label="Test Loss")
    #plt.plot(testHistoryLoss, label="Train Loss")
    plt.legend(loc='upper right')
    plt.show()



def rSquared(y_true, y_pred):
    print(r2_score(y_true, y_pred))

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
    #training_set = dataset_to_numpy[13550:48140]
    training_set = dataset_to_numpy

    training_set = np.array(training_set)
    training_set = training_set.reshape(-1, 1)
    copy_set = training_set
    print("training set \n")
    print(training_set)
    print("training set \n")
    print("data set \n")
    print(dataset)
    print("data set \n")

    #now the test data

    # Next, we will have to apply feature scaling to normalize temperature in the range 0 to 1.
    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    # we will create a training set for every 30 hours since those are the cycles of the hours and for 4 hour prediction
    x_train = []
    y_train = []

    n_future = 8  # next 12 hours
    n_past = 32  # Past 12 hours

    for i in range(0, len(training_set_scaled) - n_past - n_future + 1):
        x_train.append(training_set_scaled[i: i + n_past, 0])
        y_train.append(training_set_scaled[i + n_past: i + n_past + n_future, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #here is our rnn model which uses training data provided to learn

    loadModel = False

    if loadModel:
        regressor = pickle.load(open('finalized_model.sav', 'rb'))
        # now the test dataset
        testdata = copy_set
        real_temp = copy_set
        testdata = testdata.reshape(-1, 1)
        real_temp = real_temp.reshape(-1, 1)

        testing = sc.transform(testdata)
        testing = np.array(testing)
        testing = np.reshape(testing, (testing.shape[1], testing.shape[0], 1))

        predicted_temperature = regressor.predict(testing)
        predicted_temperature = sc.inverse_transform(predicted_temperature)
        predicted_temperature = np.reshape(predicted_temperature,
                                           (predicted_temperature.shape[1], predicted_temperature.shape[0]))

        print("real temp\n")
        print(real_temp[-n_future:])
        print("predicted temp\n")
        print(predicted_temperature)

        #print("kr nekaj?")
        #result = regressor.score(x_train, y_train)
        #print(result)

    else:
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
        history = regressor.fit(x_train, y_train, epochs=5, batch_size=32)

        #saving the model
        #filename = 'finalized_model.sav'
        #pickle.dump(regressor, open(filename, 'wb'))

        #print(f"model hist is : \n {history.history}")

        #now the test dataset
        testdata = copy_set
        real_temp = copy_set
        testdata = testdata.reshape(-1, 1)
        real_temp = real_temp.reshape(-1, 1)

        testing = sc.transform(testdata)
        testing = np.array(testing)
        testing = np.reshape(testing, (testing.shape[1], testing.shape[0], 1))

        predicted_temperature = regressor.predict(testing)
        predicted_temperature = sc.inverse_transform(predicted_temperature)
        predicted_temperature = np.reshape(predicted_temperature,(predicted_temperature.shape[1],predicted_temperature.shape[0]))

        print("real temp\n")
        print(real_temp[-n_future:])
        print("predicted temp\n")
        print(predicted_temperature)

        #evaluating model
        rSquared(real_temp[-n_future:], predicted_temperature)
        showData(history)




#rrm()
neuralnetwork()
