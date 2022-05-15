import pandas as pd
import tensorflow_decision_forests as tfdf

df = pd.read_csv("Zvezek2.csv")
print(df)

train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(df, label="Decision")

ds = pd.read_csv("Zvezek3.csv")
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(ds)


model = tfdf.keras.RandomForestModel()
model.fit(train_ds)
model.compile(metrics=["accuracy"])
#evaluation = model.evaluate(test_ds)



predictions = model.predict(
    test_ds
)

model.save("model")

for prediction in predictions:
    if(prediction < 0.5): 
        print('NO')
    else:
        print('YES')


#tfdf.model_plotter.plot_model_in_colab(model, tree_idx=0)