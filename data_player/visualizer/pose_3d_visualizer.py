import numpy as np
from matplotlib.animation import FuncAnimation
from .base_visualizer import BaseVisualizer


class Pose3DVisualizer(BaseVisualizer):
    """
    Class which helps to visualize motion capture
    pose in 3D space (matplotlib).

    :param fig: matplotlib figure
    :type fig: matplotlib.figure.Figure
    :param ax: matplotlib 3D axes
    :type ax: matplotlib.axes._subplots.Axes3DSubplot
    :param motion_capture: motion capture data
    :type motion_capture: MotionCapture
    """

    def __init__(self, fig, ax, motion_capture):
        self.fig = fig
        self.ax = ax
        self.joints = motion_capture.get_joints_reduced_by_fps(30)
        self.skeleton = motion_capture.skeleton

    def update(self, frame):
        """
        Update the animation of the matplotlib figure.

        :param frame: frame number
        :type frame: int
        """
        self.ax.clear()
        joints = self.joints[frame]

        for idx, val in enumerate(self.skeleton):
            if idx == 0:
                continue
            x_line = [joints[val - 1, 0], joints[idx, 0]]
            y_line = [joints[val - 1, 1], joints[idx, 1]]
            z_line = [joints[val - 1, 2], joints[idx, 2]]
            self.ax.plot3D(x_line, y_line, z_line, 'green')

        x = joints[:, 0].astype(int)
        y = joints[:, 1].astype(int)
        z = joints[:, 2].astype(int)

        root = 1 if np.max([x[0], y[0], z[0]]) <= 10 else 1000
        x_root, y_root, z_root = x[0], y[0], z[0]

        self.ax.set_xlim3d([-root + x_root, root + x_root])
        self.ax.set_zlim3d([-root + z_root, root + z_root])
        self.ax.set_ylim3d([-root + y_root, root + y_root])

    def get_animation(self, fps=30):
        """
        Get animation.

        :param fps: frames per second
        :type fps: int
        :return: matplotlib animation
        :rtype: matplotlib.animation.FuncAnimation
        """
        frames = np.arange(0, self.joints.shape[0])
        interval = self.joints.shape[0] / fps

        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=interval,
            repeat=False,
        )
        return anim
