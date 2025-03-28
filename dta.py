import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
import joblib

df = pd.read_csv('weather_data.csv')
df['date'] = pd.to_datetime(df['date'], format="%H:%M %d.%m.%Y")
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df = df.drop(columns=['date'])
encoder = LabelEncoder()
df['wind_direction'] = encoder.fit_transform(df['wind_direction'])
print(df['wind_direction'])
print(df.head())


x = df[['hour', 'day', 'month', 'wind_direction', 'wind_speed', "visibility", 'temp_d',
        'humidity', 'temp_e', 'temp_es', 'pressure', 'pressure_o']]
y = df['temp']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = XGBRegressor(n_estimators=10000, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Средняя абсолютная ошибка (MAE): {mae:.2f}")
joblib.dump(model, 'weather_model.pkl')
print('Model saved')