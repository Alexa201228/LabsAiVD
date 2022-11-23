"""
Лабораторная работа №5 - Регрессия.
Данная лабораторная работа содержит пример регрессионного анализа данных.
В данной ЛР в качествепримера регрессии вычисляется бета-коэффициент (рыночный риск).
Подробнее https://ru.wikipedia.org/wiki/%D0%91%D0%B5%D1%82%D0%B0-%D0%BA%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82
"""

import pandas as pd
import yfinance as yf
import numpy as np
import statsmodels.api as sm

if __name__ == '__main__':

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

    # Добавляем столбец единиц и определяем X и y
    X = sm.add_constant(return_data['IMOEX.ME'])
    y = return_data['AFLT.ME']

    # Создание модели
    model_moex = sm.OLS(y, X).fit()

    # Вывод результатов
    print(model_moex.summary())
