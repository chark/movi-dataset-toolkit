from abc import ABC, abstractmethod


class BaseVisualizer(ABC):
    """
    Base class for visualizers.
    """
    @abstractmethod
    def update(self, frame):
        """
        Update the animation of the matplotlib figure.

        :param frame: frame number
        :type frame: int
        """
        pass

    @abstractmethod
    def get_animation(self, fps=30):
        """
        Get animation.

        :param fps: frames per second
        :type fps: int
        :return: matplotlib animation
        :rtype: matplotlib.animation.FuncAnimation
        """
        pass
