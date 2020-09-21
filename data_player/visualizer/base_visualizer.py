# Python 3.4+
from abc import ABC, abstractmethod


class BaseVisualizer(ABC):
    @abstractmethod
    def update(self, frame):
        pass

    @abstractmethod
    def get_animation(self, fps=30):
        pass
