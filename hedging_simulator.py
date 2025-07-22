# hedging_simulator.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_delta_hedge(prices: pd.Series, strike: float, maturity_days: int, init_delta: float,
                          option_price_fn, delta_fn, **kwargs):
    """
    Simulate delta hedging over a price path
    """
    hedge_pnl = [0.0]
    cash = option_price_fn(prices.iloc[0], **kwargs) - init_delta * prices.iloc[0]
    position = init_delta

    for t in range(1, maturity_days):
        spot_t = prices.iloc[t]
        delta_t = delta_fn(spot_t, **kwargs)
        dS = prices.iloc[t] - prices.iloc[t - 1]
        pnl = position * dS
        hedge_pnl.append(hedge_pnl[-1] + pnl)
        cash += (position - delta_t) * spot_t  # rebalancing cost
        position = delta_t

    total_pnl = hedge_pnl[-1] + cash - option_price_fn(prices.iloc[maturity_days - 1], **kwargs)
    return hedge_pnl, total_pnl


def plot_hedging_result(pnl: list, label: str):
    plt.plot(pnl, label=label)
    plt.xlabel("Days")
    plt.ylabel("Hedging PnL")
    plt.title("Delta Hedging Simulation")
    plt.legend()
    plt.grid(True)
    plt.show()

# ダミー関数例（実装は後で差し替える）
def dummy_option_price(spot, strike, barrier, maturity_days, risk_free_rate, volatility):
    return max(spot - strike, 0) if spot > barrier else 0

def dummy_delta(spot, strike, barrier, maturity_days, risk_free_rate, volatility):
    return 0.5  # 仮置き


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("data/usdjpy_fx_data.csv", index_col=0, parse_dates=True)
    prices = df['USDJPY'].iloc[:30]

    pnl_bs, final_bs = simulate_delta_hedge(
        prices=prices,
        strike=150,
        maturity_days=30,
        init_delta=0.5,
        option_price_fn=dummy_option_price,
        delta_fn=dummy_delta,
        strike=150,
        barrier=140,
        maturity_days=30,
        risk_free_rate=0.01,
        volatility=0.15
    )

    plot_hedging_result(pnl_bs, label="BS Hedge")
    print(f"Final PnL (BS): {final_bs:.4f}")

