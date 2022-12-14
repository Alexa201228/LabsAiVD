"""
Лабораторная работа №6 - Дисперсионный анализ.
Данная лабораторная работа содержит описание применения дисперсионного анализа при
расчете остатка портфеля акций. За основу взята портфельная теория Марковица.
"""


import pandas as pd
from matplotlib.ticker import FuncFormatter
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.cla import CLA
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import pypfopt.plotting as pplt
import yfinance as yf


if __name__ == '__main__':
    tickers = ['LKOH.ME', 'GMKN.ME', 'DSKY.ME', 'NKNC.ME', 'MTSS.ME', 'IRAO.ME', 'SBER.ME', 'AFLT.ME']
    df_stocks = yf.download(tickers, start='2018-01-01', end='2022-11-01')['Adj Close']
    nullin_df = pd.DataFrame(df_stocks, columns=tickers)

    # Годовая доходность
    mu = expected_returns.mean_historical_return(df_stocks)
    # Дисперсия портфеля
    Sigma = risk_models.sample_cov(df_stocks)
    # Максимальный коэффициент Шарпа
    ef = EfficientFrontier(mu, Sigma, weight_bounds=(0, 1))  # weight bounds in negative allows shorting of stocks
    sharpe_pfolio = ef.max_sharpe()  # May use add objective to ensure minimum zero weighting to individual stocks
    sharpe_pwt = ef.clean_weights()
    print(sharpe_pwt)
    ef.portfolio_performance(verbose=True)
    ef1 = EfficientFrontier(mu, Sigma, weight_bounds=(0, 1))
    minvol = ef1.min_volatility()
    minvol_pwt = ef1.clean_weights()
    print(minvol_pwt)
    ef1.portfolio_performance(verbose=True, risk_free_rate=0.27)
    cl_obj = CLA(mu, Sigma)
    ax = pplt.plot_efficient_frontier(cl_obj, showfig=False)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    latest_prices = get_latest_prices(df_stocks)
    allocation_minv, rem_minv = DiscreteAllocation(minvol_pwt, latest_prices,
                                                   total_portfolio_value=100000).lp_portfolio()
    print(allocation_minv)
    print(f"Осталось денежных средств после построения портфеля с минимальной волатильностью составляет {rem_minv:.2f} рублей\n")


