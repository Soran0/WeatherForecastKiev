import joblib
import pandas as pd


model = joblib.load('weather_model2.pkl')


new_data = pd.DataFrame({
    'hour': [12],
    'day': [25],
    'month': [3],
    'wind_direction': [1],
    'wind_speed': [2],
    "visibility": [20000],
    'temp_d': [7.3],
    'humidity': [88],
    'temp_e': [9],
    'temp_es': [9],
    'pressure': [1014.8],
    'pressure_o': [994.6]
})

data_model2 = pd.DataFrame({
    'day': [26],
    'month': [3],
    'wind_direction': [1],
    'wind_speed': [2],
    'pressure': [1018.5],
})

predicted_temp = model.predict(data_model2)
print(f"Прогнозируемая температура: {predicted_temp[0]:.2f}°C")
