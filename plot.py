import matplotlib.pyplot as plt


def draw_plot(statistic: dict) -> plt:
    """Draws a plot based on the statistic

    Args:
        statistic (dict):

    Returns:
        plt: plt-object
    """
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel("Time")
    plt.xlabel("Number of processes")
    plt.title("Dependence of execution time on the number of processes")
    x = statistic.keys()
    y = statistic.values()
    plt.bar(x, y, color="blue", width=0.05)
    plt.show(block = False)
    return fig
