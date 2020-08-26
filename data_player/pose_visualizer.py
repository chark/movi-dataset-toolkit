from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class PoseVisualizer(object):
    def __init__(self, fig, ax, motion_capture):
        self.fig = fig
        self.ax = ax
        self.motion_capture = motion_capture

    def update(self, frame):
        self.ax.clear()
        joints = self.motion_capture.joints[frame]
        skeleton = self.motion_capture.skeleton

        for idx, val in enumerate(skeleton):
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

    def show_plot(self):
        frames = np.arange(0, self.motion_capture.joints.shape[0])
        interval = self.motion_capture.joints.shape[0] / 30

        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=interval,
            repeat=False,
        )
        # return anim
        plt.show(block=True)
