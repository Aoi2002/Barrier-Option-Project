# monte_carlo_pricer.py
import QuantLib as ql
import numpy as np


def european_knockout_call_mc(spot, strike, barrier, maturity_days, risk_free_rate, volatility,
                               num_paths=10000, seed=42):
    """
    Monte Carlo pricing for European Knock-Out Call Option under Black-Scholes model
    """
    np.random.seed(seed)

    # Dates & setup
    calendar = ql.TARGET()
    today = ql.Date.todaysDate()
    maturity_date = today + maturity_days
    day_count = ql.Actual365Fixed()

    # Option details
    payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
    exercise = ql.EuropeanExercise(maturity_date)
    option = ql.BarrierOption(ql.Barrier.DownOut, barrier, 0.0, payoff, exercise)

    # Market data
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesProcess(spot_handle, flat_ts, flat_vol_ts)

    # MC Engine
    engine = ql.MCEuropeanEngine(bsm_process, "PseudoRandom", timeSteps=1,
                                 requiredSamples=num_paths)
    option.setPricingEngine(engine)

    price = option.NPV()
    return price


# Example usage
if __name__ == "__main__":
    price = european_knockout_call_mc(
        spot=145.0,
        strike=150.0,
        barrier=140.0,
        maturity_days=30,
        risk_free_rate=0.01,
        volatility=0.15
    )
    print(f"Knock-Out Call Option Price (MC-BS): {price:.4f}")
