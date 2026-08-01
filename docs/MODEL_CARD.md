# Model Card: Hourly Consumption Forecast

## Model

The baseline implementation uses `RandomForestRegressor` with calendar, cyclical-hour, weekday, lag and rolling-average features. It is compared with a 24-hour seasonal-naive forecast.

## Intended purpose

The model demonstrates a transparent forecasting workflow that can be reproduced on demo, local or optional EPİAŞ data. It is not promoted as a production grid forecast.

## Evaluation protocol

The final 48 complete hourly records are held out. Metrics include mean absolute error and root mean squared error. The current bundled synthetic-data run produced:

- Model MAE: **716.221 MWh**
- Model RMSE: **878.652 MWh**
- Seasonal-naive MAE: **793.609 MWh**

These values describe only the bundled synthetic dataset and must not be generalized to official Turkish electricity data.

## Features

- Hour and day of week
- Weekend flag
- One-hour and 24-hour lags
- 24-hour rolling mean
- Optional 168-hour lag and rolling mean when sufficient history exists
- Sine/cosine encodings for hourly and weekly cycles

## Risks and limitations

- Random forests do not extrapolate structural shifts well.
- The validation split is chronological but short.
- Weather, holidays, outages, installed capacity and macroeconomic variables are absent from version 1.0.
- Prediction intervals are not yet implemented.
- Model monitoring and retraining policies are required before operational use.

## Recommended production extensions

Add official holiday calendars, temperature forecasts, outage information, renewable forecasts, rolling-origin cross-validation, probabilistic intervals, drift monitoring and model registry integration.
