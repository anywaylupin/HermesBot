import matplotlib.pyplot as plt
from typing import TypedDict


class GraphConfig(TypedDict):
    data_set_x: list
    data_set_y: list
    xlabel: str
    ylabel: str
    title: str
    grid: bool
    marker: str


class Plotter:
    def draw(self, config: GraphConfig):
        """
        Draws a price graph using matplotlib.

        Args:
            config: Dictionary containing graph configuration.
        """
        data_set_x = config["data_set_x"]
        data_set_y = config["data_set_y"]
        plt.figure(figsize=(10, 5))
        plt.plot(data_set_x, data_set_y, marker="o", linestyle="-", color="b")
        plt.xlabel(config["xlabel"])
        plt.ylabel(config["ylabel"])
        plt.title(config["title"])
        plt.grid(config["grid"])
        plt.show()
