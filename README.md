# Stock Price Forecasting using ARIMA with Streamlit Deployment

# Overview
This project focuses on forecasting stock prices using the ARIMA (AutoRegressive Integrated Moving Average) model. It analyzes historical stock data, identifies patterns, and predicts future prices through a deployed interactive web application.

# Problem Statement
Stock market prediction is a challenging task due to its dynamic and non-linear nature. This project aims to build a reliable time-series model to forecast future stock prices and assist in data-driven decision-making.

# Approach
1. Data Collection
Historical stock price data (e.g., Yahoo Finance)

2. Data Preprocessing
Handling missing values
Converting date column to datetime
Setting index

3. Exploratory Data Analysis (EDA)
Trend visualization
Checking stationarity

4. Model Building
Applied ARIMA model
Parameter tuning (p, d, q)
Used ACF & PACF plots

5. Forecasting
Predicted future stock prices
Visualized actual vs predicted values

7. Deployment
Built an interactive UI using Streamlit
Users can select stock and forecast duration

# Results
The ARIMA model successfully captured trends in stock price movement
Generated short-term forecasts with reasonable accuracy
Visualization shows close alignment between actual and predicted values

# Features
Time-series forecasting using ARIMA
Interactive data visualization
Web app deployment
Future price prediction

# Tech Stack
Python
Pandas, NumPy
Statsmodels
Matplotlib
Streamlit

│── data/                # Dataset files
│── notebooks/           # Jupyter notebooks (EDA & experiments)
│── model/               # Saved ARIMA model (
