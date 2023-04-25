import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from examp_data import vvsData
import pandas as pd



class MatplotlibApp:



    def __init__(self):
        self.figure, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        left_button_ax = self.figure.add_axes([0.2, 0.05, 0.1, 0.075])
        right_button_ax = self.figure.add_axes([0.7, 0.05, 0.1, 0.075])

        self.left_button = Button(left_button_ax, 'Left')
        self.right_button = Button(right_button_ax, 'Right')

        self.left_button.on_clicked(self.left_button_clicked)
        self.right_button.on_clicked(self.right_button_clicked)

    def left_button_clicked(self, event):
        print("Left button clicked")

    def right_button_clicked(self, event):
        print("Right button clicked")
        


    def plot_bar(self):
        df = pd.DataFrame(vvsData.getData())
        line_and_delay = df[["line_number", "delay"]].copy()
        group_size = line_and_delay.groupby("line_number")["delay"].transform("size")

        # Teile die Verzögerung durch die Größe jeder Gruppe, um durchschnittliche Verzögerung zu bekommen
        line_and_delay["normalized_delay"] = line_and_delay["delay"] / group_size

    
        #line_and_delay.plot.bar(x="line_number", y="delay", ax=self.ax)
        x = line_and_delay["line_number"]
        y = line_and_delay['normalized_delay']

        self.ax.bar(x, y)
        self.ax.set_title("Durchschnittliche Verspätung")
        self.ax.set_xlabel("linie")
        self.ax.set_ylabel("Verspätung in min")

        plt.show()




def main():
    app = MatplotlibApp()
    app.plot_bar()

if __name__ == "__main__":
    main()
