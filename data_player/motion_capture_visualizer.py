import numpy as np
from matplotlib.animation import FuncAnimation
import utils


class MotionCaptureVisualizer(object):
    def __init__(self, fig, ax, motion_capture, video, camera):
        self.fig = fig
        self.ax = ax
        self.image_points = utils.adapt_motion_data_for_video(
            motion_capture,
            camera
        )
        self.video = video
        self.camera = camera

    def update(self, frame):
        self.ax.clear()
        image = self.video.get_data(frame)
        self.ax.imshow(image)

        image_points = self.image_points[frame]
        x_2d = image_points[:, 0]
        y_2d = image_points[:, 1]

        self.ax.scatter(x_2d, y_2d, marker='o', label='first', s=20., c='r')

    def get_animation(self, fps=30):
        frames = np.arange(0, self.image_points.shape[0])
        interval = self.image_points.shape[0] / fps

        anim = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=interval,
            repeat=False,
        )
        return anim
