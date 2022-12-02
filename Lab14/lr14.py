"""
Лабораторная работа №14 - Моделирование.
В данной лабораторной работе использованы средства языка Python для
анализа и прогнозирования стоимости акций компаний (построение финансовой модели).
"""

from stocker.stocker import Stocker
import matplotlib.pyplot as plt

if __name__ == '__main__':

    microsoft = Stocker('MSFT')
    # Вывод графика стоимости акций компании Microsoft
    microsoft.plot_stock()
    microsoft.plot_stock(start_date='2000-01-03',  end_date='2018-01-16', stats=['Daily Change', 'Adj. Volume'],  plot_type='pct')
    microsoft.buy_and_hold(start_date='1986-03-13',
                           end_date='2018-01-16', nshares=100)
    model, model_data = microsoft.create_prophet_model()
    # model и model_data из предыдущего вызова функций
    model.plot_components(model_data)
    plt.show()
    print(microsoft.weekly_seasonality)
    microsoft.weekly_seasonality = True
    print(microsoft.weekly_seasonality)
    model, future = microsoft.create_prophet_model(days=2000)