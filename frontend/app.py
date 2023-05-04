import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from swapper import Swapper



class MainWindow:

    def __init__(self):

        self.figure, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        #Define bitton positions
        left_button_ax = self.figure.add_axes([0.2, 0.05, 0.1, 0.075])
        right_button_ax = self.figure.add_axes([0.7, 0.05, 0.1, 0.075])

        #Set buttons
        self.left_button = Button(left_button_ax, 'Left')
        self.right_button = Button(right_button_ax, 'Right')
        self.left_button.on_clicked(self.left_button_clicked)
        self.right_button.on_clicked(self.right_button_clicked)

        self.swapper = Swapper(self.ax)
        self.swapper.call_left_func()  #as initial plot call

    def left_button_clicked(self, event):
        self.ax.clear()
        self.swapper.call_left_func()
        print("Left button clicked")

    def right_button_clicked(self, event):
        self.ax.clear()
        self.swapper.call_right_func()
        print("Right button clicked")



def main():
    app = MainWindow()
    

if __name__ == "__main__":
    main()
