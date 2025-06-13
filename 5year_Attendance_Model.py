import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from tqdm import tqdm

DATA_FILE = "data/nfl_attendance_2006_2024_final.csv"
FORECAST_YEARS = [2025, 2026, 2027, 2028, 2029]
METRICS = ['home_avg', 'road_avg', 'overall_avg']
EXCLUDE_YEARS = [2020]  # years to skip for modeling

def capped(val, lower=0, upper=200_000):
    return max(lower, min(upper, val))

df = pd.read_csv(DATA_FILE)
all_results = []

for team in tqdm(df['team'].unique(), desc="Teams"):
    team_df = df[df['team'] == team].sort_values('season')
    for metric in METRICS:
        ts = team_df.set_index('season')[metric]
        # Drop 2020 (or other outlier years) from training
        ts_train = ts[~ts.index.isin(EXCLUDE_YEARS)]
        valid_points = ts_train.dropna().shape[0]
        if valid_points < 3:
            continue

        # Fit Exponential Smoothing with additive trend (trend="add")
        model = ExponentialSmoothing(ts_train, trend="add", seasonal=None, initialization_method="estimated")
        fit = model.fit(optimized=True)
        forecast = fit.forecast(len(FORECAST_YEARS))

        # Build forecast DataFrame (expected averages only)
        fcast = pd.DataFrame({
            'season': FORECAST_YEARS,
            'attendance': forecast.values,
            'type': 'forecast',
            'metric': metric,
            'team': team
        })

        # Calculate confidence intervals (using training years)
        resid_std = np.std(fit.resid)
        for i in range(1, len(FORECAST_YEARS) + 1):
            std_error = np.sqrt(resid_std ** 2 * i)
            attendance = fcast.loc[fcast.index[i-1], 'attendance']
            fcast.loc[fcast.index[i-1], 'lower'] = capped(attendance - 1.96 * std_error)
            fcast.loc[fcast.index[i-1], 'upper'] = capped(attendance + 1.96 * std_error)

        # Historical part (unchanged, includes 2020 as NaN if present)
        hist = ts.reset_index()
        hist['type'] = 'historical'
        hist['metric'] = metric
        hist['team'] = team
        hist = hist.rename(columns={metric: "attendance"})

        all_results.append(hist)
        all_results.append(fcast)

results_df = pd.concat(all_results, ignore_index=True)
results_df.to_csv("data/nfl_attendance_forecasts_2006_2029_no2020.csv", index=False)
print("Done! Forecasts saved to nfl_attendance_forecasts_2006_2029_no2020.csv")