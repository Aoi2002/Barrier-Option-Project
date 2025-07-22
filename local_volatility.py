# local_volatility.py
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, griddata
import matplotlib.pyplot as plt


def compute_local_volatility(prices: pd.Series, window: int = 20):
    """
    Compute historical volatility using rolling standard deviation
    """
    log_returns = np.log(prices / prices.shift(1))
    hist_vol = log_returns.rolling(window=window).std() * np.sqrt(252)
    return hist_vol


def create_local_vol_surface(prices: pd.Series, vol: pd.Series):
    """
    Create interpolated local volatility surface over strike and maturity
    """
    # Dummy strikes and maturities for illustration
    strikes = np.linspace(prices.min() * 0.95, prices.max() * 1.05, 10)
    maturities = np.linspace(10, 60, 6)  # in days

    grid_points = []
    grid_vols = []
    for T in maturities:
        for K in strikes:
            idx = int(T)
            if idx < len(vol):
                grid_points.append((K, T))
                grid_vols.append(vol.iloc[idx])

    surface = griddata(grid_points, grid_vols, method='linear',
                       xi=(strikes[None, :].repeat(len(maturities), axis=0),
                           maturities[:, None].repeat(len(strikes), axis=1)))

    return strikes, maturities, surface


def plot_vol_surface(strikes, maturities, surface):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(strikes, maturities)
    ax.plot_surface(X, Y, surface, cmap='viridis')
    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity (days")
    ax.set_zlabel("Local Volatility")
    ax.set_title("Local Volatility Surface")
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("data/usdjpy_fx_data.csv", index_col=0, parse_dates=True)
    prices = df['USDJPY']
    vol = compute_local_volatility(prices)
    strikes, maturities, surface = create_local_vol_surface(prices, vol)
    plot_vol_surface(strikes, maturities, surface)
