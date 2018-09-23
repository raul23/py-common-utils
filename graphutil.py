import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout


def generate_bar_chart(
        x, y, xlabel, ylabel, title, grid_which='major',
        yaxis_major_mutiplelocator=20, yaxis_minor_mutiplelocator=10):
    # Sanity check on the input arrays
    assert isinstance(x, type(np.array([]))), \
        "generate_bar_chart(): wrong type on input array 'x'"
    assert isinstance(y, type(np.array([]))), \
        "generate_bar_chart(): wrong type on input array 'y'"
    assert x.shape == y.shape, \
        "generate_bar_chart(): wrong shape with 'x' and 'y'"
    assert grid_which in ["minor", "major", "both"], \
        "generate_bar_chart(): wrong value for grid_which='{}'".format(grid_which)
    ax = plt.gca()
    index = np.arange(len(x))
    plt.bar(index, y)
    plt.xticks(index, x)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=270.)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(yaxis_major_mutiplelocator))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(yaxis_minor_mutiplelocator))
    # plt.minorticks_on()
    plt.grid(which=grid_which)
    plt.tight_layout()
    plt.show()


def generate_histogram(
        data, bins, xlabel, ylabel, title, grid_which='major',
        xaxis_major_mutiplelocator=10000, xaxis_minor_mutiplelocator=1000,
        yaxis_major_mutiplelocator=5, yaxis_minor_mutiplelocator=1):
        # TODO: `bin_width": 10000` not used
        # TODO: `xaxis_minor_mutiplelocator` not used
        # Sanity check on the input array
        assert isinstance(data, type(np.array([]))), \
            "wrong type on input array 'data'"
        assert grid_which in ["minor", "major", "both"], \
            "wrong value for grid_which='{}'".format(grid_which)
        ax = plt.gca()
        ax.hist(data, bins=bins, color="r")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(xaxis_major_mutiplelocator))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(yaxis_major_mutiplelocator))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(yaxis_minor_mutiplelocator))
        plt.xlim(0, data.max())
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=270.)
        plt.grid(True, which="major")
        plt.tight_layout()
        # TODO: add function to save image instead of showing it
        plt.show()


def generate_pie_chart(values, labels, title):
        # Sanity check on the input arrays
        assert isinstance(values, type(np.array([]))), \
            "Wrong type on input array 'values'"
        assert isinstance(labels, type(np.array([]))), \
            "Wrong type on input array 'labels'"
        assert values.shape == labels.shape, \
            "Wrong shape with 'labels' and 'values'"
        ax = plt.gca()
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title(title)
        plt.axis("equal")
        plt.show()


def generate_scatter_plot(x, y, text, title, mode='markers', hovermode='closest',
                          yaxis_tickformat='$0.0f'):
        # TODO: add labels to axes
        assert isinstance(x, type(np.array([]))), "wrong type on input array 'x'"
        assert isinstance(y, type(np.array([]))), "wrong type on input array 'y'"
        assert isinstance(text, type(np.array([]))), "wrong type on input array 'text'"
        plotly.offline.plot({
            "data": [Scatter(x=list(x.flatten()),
                             y=list(y.flatten()),
                             mode=mode,
                             text=list(text.flatten()))],
            "layout": Layout(title=title,
                             hovermode=hovermode,
                             yaxis={'tickformat': yaxis_tickformat})
        })
