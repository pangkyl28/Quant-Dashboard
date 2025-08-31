from .data import yfinance_fetch, estimate_drift, estimate_volatility
import numpy as np
import pandas as pd

def run_gbm_simulation(selected_stock, time_horizon, num_simulations):
    # Fetch historical data
    historical_data = yfinance_fetch(selected_stock)

    # Estimate drift and volatility
    drift = estimate_drift(historical_data)
    volatility = estimate_volatility(historical_data)

    S0 = float(historical_data['Close'].iloc[-1])  # Last closing price

    # Run the GBM simulation
    result = []
    for _ in range(num_simulations):
        result.append(simulate_one_gbm_path(S0, drift, volatility, time_horizon))
    
    # format
    result = np.vstack(result) # shape = (n_paths, time_horizon+1)
    # result[i, j] is price of path i on day j
    df = pd.DataFrame(
        result.T,
        columns=[f'path_{i+1}' for i in range(len(result))]
    )
    df.index.name = "day"
    
    return df

def simulate_one_gbm_path(S0, drift, volatility, time_horizon):
    dt = 1/252 # trading days in year
    path = [S0]
    for _ in range(time_horizon):
        Z = np.random.normal()
        increment = (drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * Z
        path.append(path[-1] * np.exp(increment))
    return np.array(path)
