import yfinance as yf
import numpy as np
import pandas as pd
from typing import Optional, Tuple

def yfinance_fetch(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical market data from Yahoo Finance.
    """
    return yf.download(ticker, period=period, interval=interval)


def get_log_returns(data: pd.DataFrame) -> pd.Series:
    """
    Calculate log returns from the historical price data.
    """
    return np.log(data["Close"] / data["Close"].shift(1))


def estimate_drift(data: pd.DataFrame) -> float:
    """
    Estimate the drift (mean return) of the stock.
    """
    TRADING_DAYS_PER_YEAR = 252
    log_returns = get_log_returns(data)
    return log_returns.mean().iloc[0] * TRADING_DAYS_PER_YEAR
    
def estimate_volatility(data: pd.DataFrame) -> float:
    """
    Estimate the volatility (standard deviation of returns) of the stock.
    """
    TRADING_DAYS_PER_YEAR = 252
    log_returns = get_log_returns(data)
    return log_returns.std().iloc[0] * np.sqrt(TRADING_DAYS_PER_YEAR)
