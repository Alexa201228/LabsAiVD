"""
Лабораторная работа №8 - Факторный анализ.
В данной лабораторной работе используются средства для проведения факторного анализа.
"""
import os

import pandas as pd
from sklearn.datasets import load_iris
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import matplotlib.pyplot as plt

if __name__ == '__main__':

    filename = ''
    for root, dirs, files in os.walk("./../"):
        for file in files:
            if file.startswith('bfi') and file.endswith(".csv"):
                filename = os.path.join(root, file)
    df = pd.read_csv(filename)
    df.drop(['gender', 'education', 'age'], axis=1, inplace=True)
    df.dropna(inplace=True)
    # Тест сферичности Бартлетта проверяет, коррелируют ли наблюдаемые переменные вообще, используя наблюдаемую корреляционную матрицу с единичной матрицей.
    # Если тест оказался статистически незначимым, не следует использовать факторный анализ.
    chi_square_value, p_value = calculate_bartlett_sphericity(df)
    print(chi_square_value, p_value)
    # Тест Кайзера-Мейера-Олкина (КМО) измеряет пригодность данных для факторного анализа.
    # Он определяет адекватность для каждой наблюдаемой переменной и для всей модели. KMO оценивает долю дисперсии среди всех наблюдаемых переменных.
    # Идентификатор более низкой доли больше подходит для факторного анализа. Значения KMO находятся в диапазоне от 0 до 1.
    # Значение KMO менее 0,6 считается недостаточным.
    kmo_all, kmo_model = calculate_kmo(df)
    print(kmo_all, kmo_model)
    fa = FactorAnalyzer(n_factors=25, rotation=None)
    fa.fit(df)
    # Check Eigenvalues
    ev, v = fa.get_eigenvalues()
    plt.scatter(range(1, df.shape[1] + 1), ev)
    plt.plot(range(1, df.shape[1] + 1), ev)
    plt.title('Scree Plot')
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.show()
    # Create factor analysis object and perform factor analysis using 6 factors
    fa2 = FactorAnalyzer(n_factors=6, rotation='varimax')
    fa2.fit(df)
    print(fa2.loadings_)
    # Create factor analysis object and perform factor analysis using 5 factors
    fa3 = FactorAnalyzer(n_factors=5, rotation='varimax')
    fa3.fit(df)
    print(fa3.get_factor_variance())
