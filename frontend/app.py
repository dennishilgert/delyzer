import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from plotter import Swapper
from logger import setup_logger
from plotter import VvsData



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
            * Ensure that a `MainWindow` object is created successfully, and opens the application.
            * Ensure that the left and right buttons are created and display the correct text.
            * Ensure that the initial plot is displayed correctly.
        """
        self.logger = setup_logger()

        self.figure, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.33, top=0.83, left=0.4)
        data_exporter = VvsData(self.logger)
        self.figure.canvas.manager.set_window_title('Delyzer')
        lines = data_exporter.get_lines()
        
        
        #Define bitton positions
        left_button_ax = self.figure.add_axes([0.45, 0.05, 0.1, 0.075])
        right_button_ax = self.figure.add_axes([0.75, 0.05, 0.1, 0.075])

        #Set buttons for line change
        self.buttons = []
        self.button_store_var = []
        for i, line in enumerate(lines, start=1):
            if i <= 8:
                button_ax = self.figure.add_axes([0.05, 0.87-i*0.07, 0.23, 0.055])
                button = Button(button_ax, line.line_number + ' - ' + line.direction)
                self.buttons.append(button_ax)                                                              
                self.button_store_var.append(button)          #clickable buttons have to be stored in a variable
                button.on_clicked(lambda event, line = line: self.list_button_clicked(line, event))
            else:
                self.logger.error('To many lines to show all')
                break

        #Set buttons
        self.left_button = Button(left_button_ax, 'Zurück')
        self.right_button = Button(right_button_ax, 'Weiter')
        self.left_button.on_clicked(self.left_button_clicked)
        self.right_button.on_clicked(self.right_button_clicked)

        initial_line = lines[0]
        self.swapper = Swapper(self.ax, self.buttons, initial_line, self.logger) 
        self.swapper.call_left_func()  #as initial plot call

        plt.show()  
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

    def list_button_clicked(self, line, event):
        self.logger.info('Trying to plot another line')
        self.ax.clear()
        self.swapper.switch_line(line)




def main():
    MainWindow()
    

if __name__ == "__main__":
    main()
