from plotter import Plotter
class Swapper:
    
    def __init__(self, ax) -> None:
        self.ax = ax
        self.func_pointer = 0
        self.plots = []
        self.plotter = Plotter(self.ax)

        for attr_name in dir(self.plotter):
            attr = getattr(self.plotter, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                self.plots.append(attr)
        self.func_pointer = len(self.plots)


    def call_left_func(self):
        if self.func_pointer == 0:
            self.func_pointer = len(self.plots)-1
        else:
            self.func_pointer -= 1

        self.plots[self.func_pointer]()


    def call_right_func(self):
        if self.func_pointer == len(self.plots)-1:
            self.func_pointer = 0
        else:
            self.func_pointer += 1

        self.plots[self.func_pointer]()