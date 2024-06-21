import os
import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

# Környezeti változók betöltése
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")

# Az Oracle Instant Client útvonalának beállítása
os.environ["PATH"] = "C:\\Program Files\\Oracle\\instantclient_21_14;" + os.environ["PATH"]

# Kapcsolati string létrehozása
dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, sid=DB_SID)
connection_string = f'oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{dsn}'

# SQLAlchemy engine létrehozása
engine = create_engine(connection_string)

# Adatok lekérése az adatbázisból
query = "SELECT * FROM EARTHQUAKES fetch first 1000 rows only"
df = pd.read_sql(query, con=engine)

# Adatok előfeldolgozása
features = ['latitude', 'longitude', 'depth', 'magnitude']  # Jellemző oszlopok
target = 'magnitude'  # Cél oszlop

X = df[features]  # Jellemzők
y = df[target]  # Cél változó

# Adatok felosztása tanító és teszt halmazokra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modellek inicializálása
rf_model = RandomForestRegressor(random_state=42)
nn_model = MLPRegressor(random_state=42, max_iter=1000, learning_rate_init=0.001, early_stopping=True, n_iter_no_change=10)
gb_model = GradientBoostingRegressor(random_state=42)

# Random Forest betanítása és kiértékelése
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_predictions)
print(f"Random Forest MSE: {rf_mse}")

# Neurális hálózat betanítása és kiértékelése
nn_model.fit(X_train, y_train)
nn_predictions = nn_model.predict(X_test)
nn_mse = mean_squared_error(y_test, nn_predictions)
print(f"Neural Network MSE: {nn_mse}")

# Gradient Boosting betanítása és kiértékelése
gb_model.fit(X_train, y_train)
gb_predictions = gb_model.predict(X_test)
gb_mse = mean_squared_error(y_test, gb_predictions)
print(f"Gradient Boosting MSE: {gb_mse}")

# Legjobb modell kiválasztása
mse_scores = {'Random Forest': rf_mse, 'Neural Network': nn_mse, 'Gradient Boosting': gb_mse}
best_model = min(mse_scores, key=mse_scores.get)
print(f"The best model is {best_model} with MSE: {mse_scores[best_model]}")
