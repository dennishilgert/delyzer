import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from swapper import Swapper
from logger import setup_logger



class MainWindow:
    """
    A class representing the main window of the application.

    Attributes:
        * logger (logging.Logger): The logger instance for this class.
        * figure (matplotlib.figure.Figure): The figure instance of the plot.
        * ax (matplotlib.axes.Axes): The axes instance of the plot.
        * left_button (matplotlib.widgets.Button): The button instance for left navigation.
        * right_button (matplotlib.widgets.Button): The button instance for right navigation.
        * swapper (Swapper): The instance of Swapper class to swap between plots.

    Methods:
        * __init__(self): Initializes the MainWindow class.
        * left_button_clicked(self, event): A function for left button click.
        * right_button_clicked(self, event): A function for right button click.
    """

    def __init__(self):
        """
        Creates the Mainwindow instance with a plot and buttons

        Tests:
            * Ensure that a `MainWindow` object is created successfully.
            * Ensure that the left and right buttons are created and display the correct text.
            * Ensure that the initial plot is displayed correctly.
        """
        self.logger = setup_logger()

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

        self.swapper = Swapper(self.ax, self.logger)
        self.swapper.call_left_func()  #as initial plot call
        plt.show()    # needed to make .draw functions work
        self.logger.info('Closed window')

    def left_button_clicked(self,event):
        """
        Change plot.

        Args:
            event (_type_): _description_
        
        Tests:
            * Test if the plot gets cleared correctly
            * Test if next plot appeares
        """
        self.logger.info('Trying to plot next plot')
        self.ax.clear()
        self.swapper.call_left_func()

    def right_button_clicked(self, event):
        """
        Change plot.

        Args:
            event (_type_): _description_
        
        Tests:
            * Test if the plot gets cleared correctly
            * Test if previous plot appeares
        """
        self.logger.info('Trying to plot previous plot')
        self.ax.clear()
        self.swapper.call_right_func()



def main():
    MainWindow()
    

if __name__ == "__main__":
    main()
