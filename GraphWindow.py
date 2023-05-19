#GraphWindow.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class GraphWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Graph Window")
        self.figure, self.ax = plt.subplots()
        self.graph = FigureCanvasTkAgg(self.figure, self.window)
        self.graph.get_tk_widget().pack()

    def plot_data(self, data):
        self.ax.clear()
        self.ax.plot(data)
        self.graph.draw()
