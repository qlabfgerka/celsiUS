import pandas as pd
import tensorflow_decision_forests as tfdf


def predict(input):
    df = pd.read_csv("Zvezek2.csv")
    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(df, label="Decision")


    print(input)

    test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(input)

    model = tfdf.keras.RandomForestModel()
    model.fit(train_ds)

    predictions = model.predict(
      test_ds
    )

    for prediction in predictions:
      if(prediction < 0.5): 
          return 'NO'
      else:
          return 'YES'




