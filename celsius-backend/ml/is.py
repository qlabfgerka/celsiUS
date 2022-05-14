import pandas as pd


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
    core_weather = weather[["TMAX", "TMIN"]].copy()
    core_weather.columns = ["tempmax", "tempmin"]

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
    core_weather = core_weather.iloc[:-1,:].copy()
    core_weather["target"] = core_weather.shift(-1)["tempmax"]
    print(core_weather)

rrm()
