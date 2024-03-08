import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from datetime import datetime

import calmap
import os
import pandas as pd
import numpy as np

from init import TZ, log_error
from db import DailyStressData


CMAP = LinearSegmentedColormap.from_list (
    name='stress',
    colors=['#5f3566', '#d80af7', '#1d30de', '#40ebf7', '#fff', '#05fa3a', '#fae105', '#ff7b00', '#ff3b00'],
    N=512)


# график по дням
def get_daily_stress_plot(user_id: int, data: tuple[DailyStressData]):
    df_work = pd.DataFrame (data, columns=['date', 'day_rating'])
    df_work ['date'] = pd.to_datetime (df_work ['date'])
    df_work.set_index ('date', inplace=True)
    df_work ['day_rating'] = df_work ['day_rating'].astype (np.int32)

    plt.figure (figsize=(16, 10), dpi=80)

    current_year = datetime.now(TZ).year
    calmap.yearplot(
        data=df_work,
        year=current_year,
        cmap=CMAP
    )
    file_path = os.path.join ('temp', f'daily_{user_id}.jpg')
    plt.savefig (file_path, format='jpg', dpi=200)


# глобальный график
def get_global_stress_plot(user_id: int, happy: int, unhappy: int):
    def normal_pdf(x, mean, var_):
        return np.exp (-(x - mean) ** 2 / (2 * var_))

    xmin, xmax, ymin, ymax = (0, 100, 0, 100)
    n_bins = 100
    xx = np.linspace (xmin, xmax, n_bins)
    yy = np.linspace (ymin, ymax, n_bins)

    means_high = [60, 40]
    means_low = [40, 60]

    var = [happy, unhappy]

    gauss_x_high = normal_pdf (xx, means_high [0], var [0])
    gauss_y_high = normal_pdf (yy, means_high [1], var [0])

    gauss_x_low = normal_pdf (xx, means_low [0], var [1])
    gauss_y_low = normal_pdf (yy, means_low [1], var [1])

    weights = (np.outer (gauss_y_high, gauss_x_high)
               - np.outer (gauss_y_low, gauss_x_low))

    greys = np.full ((*weights.shape, 3), 70, dtype=np.uint8)

    vmax = np.abs (weights).max ()
    imshow_kwargs = {
        'vmax': vmax,
        'vmin': -vmax,
        'cmap': CMAP,
        'extent': (xmin, xmax, ymin, ymax),
    }

    fig, ax = plt.subplots ()
    ax.imshow (greys)
    ax.imshow (weights, **imshow_kwargs)
    ax.set_axis_off ()

    # plt.switch_backend ('Agg')
    plt.switch_backend ('GTK3Cairo')

    file_path = os.path.join ('temp', f'global_{user_id}.jpg')
    plt.savefig (file_path, format='jpg', dpi=500)
