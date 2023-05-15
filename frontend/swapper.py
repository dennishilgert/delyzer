from plotter import Plotter
class Swapper:
    
    def __init__(self, ax, button_list, initial_line, logger) -> None:
        """
    Initializes the instance with a provided matplotlib axes and a Plotter object.

    Args:
        ax (matplotlib.axes.Axes): The matplotlib axes used for plotting.


    Side Effects:
        * Sets the 'ax' attribute to the provided matplotlib axes.

    Tests:
        * Test that the function initializes the attributes correctly.
        * Test that the 'plots' list is populated with callable methods from the Plotter object.
        * Test that the 'func_pointer' attribute is set to the length of the 'plots' list.
    """
        self.ax = ax
        self.func_pointer = 0
        self.plots = []
        self.plotter = Plotter(self.ax, button_list, initial_line, logger)

        for attr_name in dir(self.plotter):
            attr = getattr(self.plotter, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                self.plots.append(attr)
        self.func_pointer = len(self.plots)


    def call_left_func(self):
        """
        Calls the function to the left of the current 'func_pointer' in the 'plots' list.

        Tests:
            * Test that the function updates the 'func_pointer' attribute correctly when not at the beginning of the list.
            * Test that the function wraps around to the end of the list when the 'func_pointer' is at the beginning.
            * Test that the function at the updated 'func_pointer' index is called.
        """
        if self.func_pointer == 0:
            self.func_pointer = len(self.plots)-1
        else:
            self.func_pointer -= 1

        self.plots[self.func_pointer]()


    def call_right_func(self):
        """
        Calls the function to the right of the current 'func_pointer' in the 'plots' list.

        Tests:
            * Test that the function updates the 'func_pointer' attribute correctly when not at the end of the list.
            * Test that the function wraps around to the beginning of the list when the 'func_pointer' is at tend.
            * Test that the function at the updated 'func_pointer' index is called.
        """
        if self.func_pointer == len(self.plots)-1:
            self.func_pointer = 0
        else:
            self.func_pointer += 1

        self.plots[self.func_pointer]()

    def switch_line(self, new_line):
        self.plots[self.func_pointer](new_line)