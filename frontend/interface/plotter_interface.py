from abc import ABC, abstractmethod

class PlotterInterface(ABC):
    
    @abstractmethod
    def plot_avg_line_delay(self):
        pass
    
    @abstractmethod
    def plot_avg_time_delay(self):
        pass
    __all__ = ["PlotterInterface"]

    