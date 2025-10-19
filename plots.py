import matplotlib.pyplot as plt
import numpy as np


def plot_time_distribution(stats_df, step: float, metric='lost clients'):
    df = stats_df.copy(deep=True)

    # Create time in decimal hours (10.0, 10.25, 10.5, etc.)
    aggregated = group_df_by_time(stats_df, metric)

    # Group by time and calculate average, median, min, max
    mean_vals = aggregated.mean()
    median_vals = aggregated.median()
    min_vals = aggregated.min()
    max_vals = aggregated.max()

    y_top_limit = max_vals.values.max()

    fig, axes = plt.subplots(ncols=2, nrows=2, constrained_layout=True)
    x_shift = step / 2

    fig.suptitle(
        f'{metric.title()} by Time ({df['datetime'].dt.date.nunique()} days)', fontsize=16, color='darkblue')

    # Plot Average
    create_bar(axes[0, 0], y_top_limit, mean_vals.index + x_shift,
               mean_vals.values, metric, 'average', '#348ddb')
    # Plot Mean
    create_bar(axes[0, 1], y_top_limit, median_vals.index + x_shift,
               median_vals.values, metric, 'median', '#db9034')
    # Plot Min
    create_bar(axes[1, 0], y_top_limit, min_vals.index + x_shift,
               min_vals.values, metric, 'min', '#52f65b')
    # Plot Max
    create_bar(axes[1, 1], y_top_limit, max_vals.index + x_shift,
               max_vals.values, metric, 'max', '#db5534')

    plt.show()


def create_bar(ax, y_top,  x_values, y_values, metric, measure: str, colorHex: str):
    ax.bar(x_values, y_values, width=0.2,
           alpha=0.8, color=colorHex, edgecolor='black')
    ax.set_xlabel('Time of Day (hours)', fontsize=12)
    ax.set_ylabel(f'{measure.title()} {metric.title()}', fontsize=12)
    ax.set_title(measure.title(),
                 fontsize=14, fontweight='bold')
    ax.set_xlim(9.5, 20.5)
    ax.set_ylim(0, y_top + y_top / 10)
    ax.grid(True, alpha=0.3, axis='y')


def plot_distribution(stats_df, metric='products'):
    df = stats_df.copy(deep=True)

    plt.figure(figsize=(8, 5))
    data = df[metric]

    plt.hist(
        data,
        bins=np.arange(data.min(), data.max() + 2) -
        0.5,
        color='#db5b34',
        edgecolor="#963e23",
        rwidth=1.0,
        zorder=2
    )

    plt.xticks(range(data.min(), data.max() + 1))
    plt.xlabel(f'Number of {metric.title()}')
    plt.ylabel('Frequency')
    plt.title(f'{metric.title()} Distribution')
    plt.grid(True, zorder=1)

    plt.show()


def plot_line(stats_df, metric='throughput'):
    plt.figure(figsize=(8, 5))

    aggregated = group_df_by_time(stats_df, metric)
    data = aggregated.mean()
    y_top = data.values.max()
    y_bottom = data.values.min()
    plt.plot(data.index, data.values,
             alpha=1, color='magenta')
    plt.xlabel('Time of Day (hours)', fontsize=12)
    plt.ylabel(f'Average {metric.title()}', fontsize=12)
    plt.title('Average',
              fontsize=14, fontweight='bold')
    plt.xlim(9.5, 20.5)
    plt.ylim(y_bottom, y_top + (y_top - y_bottom) / 10)
    plt.grid(True, alpha=0.3)

    plt.show()


def group_df_by_time(stats_df, metric):
    df = stats_df.copy(deep=True)
    df['hour'] = df['datetime'].dt.hour + df['datetime'].dt.minute / 60
    return df.groupby('hour')[metric]
