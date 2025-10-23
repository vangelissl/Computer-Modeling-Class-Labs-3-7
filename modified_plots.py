import matplotlib.pyplot as plt


def plot_scatter(df, metric, ax):
    values = df.loc[metric].values

    # Create list of workers (x-axis)
    workers = list(df.columns.astype(str))

    # Plot scatter
    ax.scatter(workers, values, s=70, color='magenta', zorder=2)

    ax.set_title(f'{metric.title()} by Number of Workers')
    ax.set_xlabel('Number of Workers')
    ax.set_ylabel('A')
    ax.grid(True, zorder=1)


def plot_bar(df, metric, ax):
    values = df.loc[metric].values

    # Create list of workers (x-axis)
    workers = list(df.columns.astype(str))

    # Plot scatter
    ax.bar(workers, values, color="#e86637", width=0.7, zorder=2)

    ax.set_title(f'{metric.title()} by Number of Workers')
    ax.set_xlabel('Number of Workers')
    ax.set_ylabel(metric.title())
    ax.grid(True, zorder=1)


def plot_metrics(df, title):
    fig, axes = plt.subplots(2, 2)

    fig.suptitle(
        f'{title.title()}', fontsize=16, color='darkblue')

    plot_scatter(df, 'A', axes[0][0])
    plot_bar(df, 'p_refusal', axes[1][0])
    plot_scatter(df, 'L_q', axes[0][1])
    plot_bar(df, 'idle', axes[1][1])

    plt.tight_layout()
    plt.show()
