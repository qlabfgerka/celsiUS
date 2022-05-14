import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

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




rrm()
