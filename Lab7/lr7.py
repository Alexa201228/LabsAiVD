"""
Лабораторная № 7 - Анализ мощности.
Данная лабораторная работа содержит код анализа мощности выборки
данных в финансовой сфере.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot
from statsmodels.stats.power import TTestPower
import yfinance as yf

if __name__ == '__main__':
    # parameters for power analysis
    ticker = ['AFLT.ME', 'IMOEX.ME']
    stock = yf.download(ticker)

    # Выделение скорректированой цены закрытия
    all_adj_close = stock[['Adj Close']]

    # Вычисление доходности
    all_returns = np.log(all_adj_close / all_adj_close.shift(1))

    # Выделение доходности по акциям
    aflt_returns = all_returns['Adj Close'][['AFLT.ME']].fillna(0)

    # Выделение доходности по индексу МосБиржи
    moex_returns = all_returns['Adj Close'][['IMOEX.ME']].fillna(0)

    # Создание нового DataFrame

    return_data = pd.concat([aflt_returns, moex_returns], axis=1)[1:]
    return_data.columns = ['AFLT.ME', 'IMOEX.ME']
    effect_sizes = np.array([0.2, 0.5, 0.8])
    return_data = return_data.drop(return_data[return_data['IMOEX.ME'] > 5].index)['IMOEX.ME']
    sample_sizes = np.array(range(5, len(return_data)))
    # calculate power curves from multiple power analyses
    analysis = TTestPower()
    analysis.plot_power(dep_var='nobs', nobs=sample_sizes, effect_size=effect_sizes)
    pyplot.show()
    power_of_sample_dataset = analysis.solve_power(nobs=len(return_data) // 100, effect_size=0.5, power=None, alpha=0.05)
    print(power_of_sample_dataset)
