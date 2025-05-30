# -*- coding: utf-8 -*-
"""Multiple Linear Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12P7HRMzANhfKiZx8kvAbd8d7qYNUBebo
"""

import numpy as np
import pandas as pd
df = pd.read_csv("/content/cars.csv")
df.head()

print("Missing Values Before Handling:")
print(df.isnull().sum())
print(df.shape)
print("Number of rows",df.shape[0])
print("Number of columns",df.shape[1])
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
print("Numerical Variables in the Dataset:")
print(numerical_columns)
categorical_columns=df.select_dtypes(include=['object']).columns
print("cat Variables in the Dataset:")
print(categorical_columns)

"""**Finding the duplicated rows in the dataset**"""

num_duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {num_duplicates}")
df_cleaned = df.drop_duplicates()
print(df_cleaned.shape)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['Engine Information.Driveline'] = le.fit_transform(df['Engine Information.Driveline'])
df['Identification.Classification'] = le.fit_transform(df['Identification.Classification'])
df['Engine Information.Hybrid'] = le.fit_transform(df['Engine Information.Hybrid'])

X = df[['Engine Information.Driveline', 'Engine Information.Hybrid', 'Identification.Classification',
        'Engine Information.Engine Statistics.Horsepower', 'Engine Information.Engine Statistics.Torque']]

y = df['Fuel Information.City mpg']

from sklearn.model_selection import train_test_split

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Data Size:", X_train.shape)
print("Testing Data Size:", X_test.shape)

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)

# Get Coefficients & Intercept
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = model.predict(X_test)

# Calculate Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))


sns.scatterplot(x=y_test, y=y_pred, color='blue', alpha=0.6)

plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='dashed')

plt.xlabel("Actual City MPG")
plt.ylabel("Predicted City MPG")
plt.title("Actual vs. Predicted City MPG")


plt.show()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_train = scaler.fit_transform(X_train)

import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
X_train_sm = sm.add_constant(X_train)
model_sm = sm.OLS(y_train, X_train_sm).fit()

# 1. Linearity: Check scatter plots of predictors vs. target
sns.pairplot(df, x_vars=['Engine Information.Engine Statistics.Horsepower', 'Engine Information.Engine Statistics.Torque'], y_vars=['Fuel Information.City mpg'])
plt.show()

# 2. Independence: Assumed based on data collection (not explicitly checked)

# 3. Homoscedasticity: Check residuals vs. fitted values plot
plt.scatter(model_sm.fittedvalues, model_sm.resid)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs. Fitted Values (Homoscedasticity Check)")
plt.show()

# 4. Normality: Check Q-Q plot of residuals
sm.qqplot(model_sm.resid, line='s')
plt.title("Q-Q Plot (Normality Check)")
plt.show()

# 5. Multicollinearity: Check Variance Inflation Factor (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = [variance_inflation_factor(X_train_sm, i) for i in range(X_train_sm.shape[1])]
print("VIF:", vif)